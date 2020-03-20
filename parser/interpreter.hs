-- Custom version of simple interpreter, modified simple.hs a bit
import qualified Data.Map as Map

data Expr = Num Integer     -- One very basic example, where expression is a constant integer
          | Bin Operator Expr Expr -- Binary opeartion between two expressions
          | Var String      -- Variable
          | Let [(String, Expr)] Expr   -- Let [(name, rhs), ...] eval-me (let... in...)
          | Cond Expr Expr Expr         -- Cond test then-branch else-branch
    deriving(Show)

data Operator = Plus | Multiply | Minus     -- Three operators support only, +, -, x
    deriving(Show)

data Value = VNum Integer   -- Integer value
           | VBool Bool     -- Boolean value
    deriving(Show)

interpret :: Expr -> Map.Map String Value -> Either String Value
-- The most basic interpretation is to convert integer from expression to value
interpret (Num i) _ = pure (VNum i)
-- expr plus expr
interpret (Bin Plus left right) env = 
    -- Interpret left expression first
    interpret left env
    -- Then try to convert the result to an integer
    >>= \a -> tryInt a
    -- Then inpterpret the right expreesion
    >>= \b -> interpret right env
    -- Then try to convert the result to an integer
    >>= \c -> tryInt c
    -- Apply addition
    >>= \d -> return (VNum (b + d))
-- expr minus expr
interpret (Bin Minus left right) env = 
    -- Interpret left expression first
    interpret left env
    -- Then try to convert the result to an integer
    >>= \a -> tryInt a
    -- Then inpterpret the right expreesion
    >>= \b -> interpret right env
    -- Then try to convert the result to an integer
    >>= \c -> tryInt c
    -- Apply addition
    >>= \d -> return (VNum (b - d))
-- expr multiply expr
interpret (Bin Multiply left right) env = 
    -- Interpret left expression first
    interpret left env
    -- Then try to convert the result to an integer
    >>= \a -> tryInt a
    -- Then inpterpret the right expreesion
    >>= \b -> interpret right env
    -- Then try to convert the result to an integer
    >>= \c -> tryInt c
    -- Apply addition
    >>= \d -> return (VNum (b * d))
-- var str: Reading variable from environment
interpret (Var v) env = case Map.lookup v env of
    Just a -> pure a
    Nothing -> raise "variable not found"
-- let ... in ...
interpret (Let eqns evalMe) env =
    extend eqns env
        >>= \env' -> interpret evalMe env'
    where
        -- extend: return an environment with variables stored
        -- If no variable assignments are given, return the environment
        extend [] env = return env
        -- If variable assignment is presented, v=variable name, rhs=right hand side expression
        extend ((v,rhs) : eqns) env =
            -- Interpret the right hand side with the original environment - env
            interpret rhs env
            -- Then get the result from last interpretation,
            -- return env' which is a map after inserting v=variable name and a=interpretation result
            -- Keep extending with new environment
            >>= \a -> let env' = Map.insert v a env in extend eqns env'
-- Cond test then else
interpret (Cond test eThen eElse) env =
    -- Interpreting the test expression and compare True and False
    interpret test env
    >>= \a -> case a of
      VBool True -> interpret eThen env
      VBool False -> interpret eElse env
      _ -> raise "type error"

-- Try to convert a Value to an integer, if fail, raise the error
-- And the Left will contains the error message
tryInt :: Value -> Either String Integer
tryInt (VNum i) = pure i
tryInt _ = raise "type error"

-- Raise an error with message
raise :: String -> Either String a
raise = Left

main = do
    let five = Num 5
    let fiften = Num 15
    let six = Num 6
    let ten = Num 10
    let seven = Num 7
    -- Expression: Num 7 -> 7
    print(interpret seven Map.empty)
    -- Expression: Num 10 + Num 15 -> 25
    let expr1 = Bin Plus ten fiften
    print(interpret expr1 Map.empty)
    -- Expression: (Num 10) + ((Num 5) + (Num 6)) -> 21
    let expr2 = Bin Plus ten (Bin Plus five six)
    print(interpret expr2 Map.empty)
    -- Expression: Num 10 * (Num 5 - (Num 7 + Num 6)) = -80
    let expr3 = Bin Multiply ten (Bin Minus five (Bin Plus seven six))
    print(interpret expr3 Map.empty)
    -- Expression: Let x = 5, y = 10 in x + y -> 15
    let expr4 = Let [("x", five), ("y", ten)] (Bin Plus (Var "x") (Var "y"))
    print(interpret expr4 Map.empty)
    -- Expression Let x = 5 in x + y -> should raise error
    let expr5 = Let [("x", five)] (Bin Plus (Var "x") (Var "y"))
    print(interpret expr5 Map.empty)