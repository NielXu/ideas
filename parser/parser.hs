-- A simple parser, parse a string into an AST
import Data.Char
import Control.Applicative

data Parser a = MkParser (String -> Maybe (String, a))

instance Functor Parser where
    -- fmap :: (a -> b) -> Parser a -> Parser b
    fmap f (MkParser sf) = MkParser sfb
      where
        sfb inp = case sf inp of
                    Nothing -> Nothing
                    Just (rest, a) -> Just (rest, f a)
                  -- OR: fmap (\(rest, a) -> (rest, f a)) (sf inp)

instance Applicative Parser where
    -- pure :: a -> Parser a
    pure a = MkParser (\inp -> Just (inp, a))

    -- liftA2 :: (a -> b -> c) -> Parser a -> Parser b -> Parser c
    -- Consider the 1st parser to be stage 1, 2nd parser stage 2.
    liftA2 op (MkParser sf1) p2 = MkParser g
      where
        g inp = case sf1 inp of
                  Nothing -> Nothing
                  Just (middle, a) ->
                      case unParser p2 middle of
                        Nothing -> Nothing
                        Just (rest, b) -> Just (rest, op a b)

instance Monad Parser where
    -- return :: a -> Parser a
    return = pure

    -- (>>=) :: Parser a -> (a -> Parser b) -> Parser b
    MkParser sf1 >>= k = MkParser g
      where
        g inp = case sf1 inp of
                  Nothing -> Nothing
                  Just (rest, a) -> unParser (k a) rest

instance Alternative Parser where
    -- empty :: Parser a
    -- Always fail.
    empty = MkParser (\_ -> Nothing)

    -- (<|>) :: Parser a -> Parser a -> Parser a
    -- Try the 1st one. If success, done; if failure, do the 2nd one
    MkParser sf1 <|> p2 = MkParser g
      where
        g inp = case sf1 inp of
                  Nothing -> unParser p2 inp
                  j -> j        -- the Just case

    -- many :: Parser a -> Parser [a]
    -- 0 or more times, maximum munch, collect the answers into a list.
    -- Can use default implementation. And it goes as:
    many p = some p <|> pure []
    -- How to make sense of it: To repeat 0 or more times, first try 1 or more
    -- times!  If that fails, then we know it's 0 times, and the answer is the
    -- empty list.

    -- some :: Parser a -> Parser [a]
    -- 1 or more times, maximum munch, collect the answers into a list.
    -- Can use default implementation. And it goes as:
    some p = liftA2 (:) p (many p)
    -- How to make sense of it: To repeat 1 or more times, do 1 time, then 0 or
    -- more times!  Use liftA2 to chain up and collect answers.

-- Apply parser to a string, return a tuple (rest, parsed)
unParser :: Parser a -> String -> Maybe (String, a)
unParser (MkParser sf1) = sf1

-- Run the parser to a string, return only the result
runParser :: Parser a -> String -> Maybe a
runParser (MkParser sf) inp = case sf inp of
                                Nothing -> Nothing
                                Just (_, a) -> Just a
                              -- OR: fmap (\(_,a) -> a) (sf inp)

-- Get a single char from the string, return Nothing if the string is empty
anyChar :: Parser Char
anyChar = MkParser sf
    where
        sf "" = Nothing
        sf (c:cs) = Just (cs, c)

-- Get a specific char from the string, return Nothing if it is not matched or empty
char :: Char -> Parser Char
char wanted = MkParser sf
    where
        sf (c:cs) | c == wanted = Just (cs, c)
        sf _ = Nothing

-- Get a char if it satisfies the predicate, return Nothing if it is not
satisfy :: (Char -> Bool) -> Parser Char
satisfy pred = MkParser sf
    where
        sf (c:cs) | pred c = Just (cs, c)
        sf _ = Nothing

-- Return an empty tuple if it is the end of the string, Nothing otherwise
eof :: Parser ()
eof = MkParser sf
    where
        sf "" = Just ("", ())
        sf _ = Nothing

-- | Space or tab or newline (unix and windows).
whitespace :: Parser Char
whitespace = satisfy (\c -> c `elem` ['\t', '\n', '\r', ' '])

-- | Consume zero or more whitespaces, maximum munch.
whitespaces :: Parser String
whitespaces = many whitespace

-- | Read a natural number (non-negative integer), then skip trailing spaces.
natural :: Parser Integer
natural = fmap read (some (satisfy isDigit)) <* whitespaces
-- read :: Read a => String -> a
-- For converting string to your data type, assuming valid string.  Integer
-- is an instance of Read, and our string is valid, so we can use read.

-- | Read an identifier, then skip trailing spaces.  Disallow the listed keywords.
identifier :: [String] -> Parser String
identifier keywords =
    satisfy isAlpha
    >>= \c -> many (satisfy isAlphaNum)
    >>= \cs -> whitespaces
    >> let str = c:cs
    in if str `elem` keywords then empty else return str

-- | Read the wanted keyword, then skip trailing spaces.
keyword :: String -> Parser String
keyword wanted =
    satisfy isAlpha
    >>= \c -> many (satisfy isAlphaNum)
    >>= \cs -> whitespaces
    *> if c:cs == wanted then return wanted else empty

-- | Read the wanted operator, then skip trailing spaces.
operator :: String -> Parser String
operator wanted =
    anyOperator
    >>= \sym -> if sym == wanted then return wanted else empty

anyOperator :: Parser String
anyOperator = some (satisfy symChar) <* whitespaces
  where
    symChar c = c `elem` "=/<>&|+-*%!\\"

data Expr
    = Num Integer
    | Var String
    | Prim2 Op2 Expr Expr       -- Prim2 op operand operand
    | Let [(String, Expr)] Expr -- Let [(name, rhs), ...] body
    deriving(Show)

data Op2 = Add | Mul
    deriving(Show)

chainr1 :: Parser a               -- ^ operand parser
        -> Parser (a -> a -> a)   -- ^ operator parser
        -> Parser a               -- ^ whole answer
chainr1 getArg getOp = liftA2 link
                       getArg
                       (optional
                         (liftA2 (,) getOp (chainr1 getArg getOp)))
  where
    link x Nothing = x
    link x (Just (op,y)) = op x y

-- | Open and close parentheses.
openParen, closeParen :: Parser Char
openParen = char '(' <* whitespaces
closeParen = char ')' <* whitespaces

-- | One or more operands separated by an operator. Apply the operator(s) in a
-- left-associating way.
chainl1 :: Parser a               -- ^ operand parser
        -> Parser (a -> a -> a)   -- ^ operator parser
        -> Parser a               -- ^ whole answer
chainl1 getArg getOp = liftA2 link
                       getArg
                       (many (liftA2 (,) getOp getArg))
    where
        link x opys = foldl (\accum (op,y) -> op accum y) x opys

mulsRv2 :: Parser Expr
mulsRv2 = chainr1 (fmap Num natural) (operator "*" *> pure (Prim2 Mul))

lesson4 :: Parser Expr
lesson4 = whitespaces *> expr <* eof
    where
        expr = local <|> adds

        local = pure (\_ eqns _ e -> Let eqns e)
            <*> keyword "let"
            <*> many equation
            <*> keyword "in"
            <*> expr
        -- Basically a liftA4.
        -- Could also be implemented in monadic style, like equation below.

        equation = var
            >>= \v -> operator "="
            >> expr
            >>= \e -> semicolon
            >> return (v, e)
        -- Basically a liftA4.
        -- Could also be implemented in applicative style, like local above.
        semicolon = char ';' *> whitespaces
        adds = chainl1 muls (operator "+" *> pure (Prim2 Add))
        muls = chainl1 atom (operator "*" *> pure (Prim2 Mul))
        atom = fmap Num natural
           <|> fmap Var var
           <|> (openParen *> expr <* closeParen)
        var = identifier ["let", "in"]

main = do
    print(runParser anyChar "abc")
    print(runParser (char 'a') "abc")
    print(runParser (satisfy isAlpha) "abc")
    print(runParser eof "")
    -- Applying two parsers
    -- <* (char '!') will check if the last one is '!' and drop it
    let lde = liftA2 (\x y -> [x,y]) (satisfy isAlpha) (satisfy isDigit) <* (char '!') :: Parser String
    print(runParser lde "B6!")
    print(runParser lde "B6a")
    -- Applying three parsers
    -- <* (char '!') will check if the last one is '!' and drop it
    let lde2 = pure (\x y z -> [x, y, z]) <*> (satisfy isAlpha) <*> (satisfy isDigit) <*> (satisfy isDigit) <* (char '!') :: Parser String
    print(runParser lde2 "B61!")
    print(runParser lde2 "B666")
    -- Using <|> to check multiple possibilities
    let ab01 = liftA2 (\x y -> [x,y]) (char 'A' <|> char 'B') (char '0' <|> char '1') :: Parser String
    print(runParser ab01 "A0")
    print(runParser ab01 "AB")
    -- many: 0 or more times, return empty string if it is 0 times
    let m = many (char 'A' <|> char 'B')
    print(runParser m "ABAC")
    print(runParser m "CDCD")
    -- some: 1 or more times, return Nothing if it is 0 times
    let s = some (char 'A' <|> char 'B')
    print(runParser s "ABAC")
    print(runParser s "CDCD")
    -- whitespace: match one whitespace
    print(runParser whitespace " ")
    print(runParser whitespace "AA")
    -- whitespaces: match zero or more whitespaces, return empty string if
    -- there is no whitespace
    print(runParser whitespaces "     ")
    print(runParser whitespaces "AA")
    -- natural: get a natural number, Nothing if it is not a natural number
    print(runParser natural "123!")
    print(runParser natural "!123")
    -- identifier: get string before first whitespace or an identifier
    -- Nothing if the first identifier is disallowed
    print(runParser (identifier ["while", "let"]) "let x = 3 in x + y")
    print(runParser (identifier ["while"]) "let x = 3")
    -- keyword: get the given keyword if it exists
    -- Nothing if the keyword does not match
    print(runParser (keyword "let") "let x = 3 in x + y")
    print(runParser (keyword "while") "let x = 3 in x + y")
    -- Parse Mul
    print(runParser mulsRv2 "3*2*1")
    -- final parser
    print(runParser lesson4 "let x=3; in x+6")