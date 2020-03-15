-- This is an example from the course note
-- http://www.cs.utoronto.ca/~trebla/CSCC24-2020-Winter/09-semantics-1.html
import qualified Data.Map as Map

data Expr = Num Integer
          | Bln Bool
          | Prim2 Op2 Expr Expr         -- Prim2 op operand operand
          | Cond Expr Expr Expr         -- Cond test then-branch else-branch
          | Var String
          | Let [(String, Expr)] Expr   -- Let [(name, rhs), ...] eval-me
          | Lambda String Expr          -- Lambda var body
          | VClosure (Map.Map String Value) String Expr
          | App Expr Expr               -- App func param
          | LetRecFun String String Expr Expr -- LetRecFun funcname paramname funcbody eval-me

data Value = VN Integer
           | VB Bool

data Op2 = Eq | Plus | Mul

mainInterp :: Expr -> Either String Value
-- Start interpret feeding the expression(expr) and an empty map(Map.empty)
-- The purpose of the map is to save all the variables
mainInterp expr = interp expr Map.empty

interp :: Expr -> Map.Map String Value -> Either String Value
-- If expression is a number, return the number value
interp (Num i) _ = pure (VN i)
-- If expression is an addition expression
interp (Prim2 Plus e1 e2) env =
    interp e1 env
    >>= \a -> intOrDie a
    >>= \i -> interp e2 env
    >>= \b -> intOrDie b
    >>= \j -> return (VN (i+j))
-- If expression is an boolean expression
interp (Cond test eThen eElse) env =
    interp test env
    >>= \a -> case a of
      VB True -> interp eThen env
      VB False -> interp eElse env
      _ -> raise "type error"
-- Lookup the variable from the environment
interp (Var v) env = case Map.lookup v env of
  Just a -> pure a
  Nothing -> raise "variable not found"
-- Create new variable
interp (Let eqns evalMe) env =
    extend eqns env
    >>= \env' -> interp evalMe env'
    -- Example:
    --    let x=2+3; y=x+4 in x+y
    -- -> x+y   (with x=5, y=9 in the larger environment env')
    -- "extend env eqns" builds env'
  where
    extend [] env = return env
    extend ((v,rhs) : eqns) env =
        interp rhs env
        >>= \a -> let env' = Map.insert v a env
                  in extend eqns env'
-- A closure is a record or data structure that stores an expression
interp (Lambda v body) env = pure (VClosure env v body)
-- If expression is a function
interp (App f e) env =
    interp f env
    >>= \c -> case c of
      VClosure fEnv v body ->
          interp e env
          >>= \eVal -> let bEnv = Map.insert v eVal fEnv  -- fEnv, not env
                       in interp body bEnv
          -- E.g.,
          --    (\y -> 10+y) 17
          -- -> 10 + y      (but with y=17 in environment)
          --
      _ -> raise "type error"
-- Recursion
interp (LetRecFun f v fbody evalMe) env =
    let closure = VClosure env' v fbody
        env' = Map.insert f closure env
    in interp evalMe env'

-- Convert a value to int or raise an error
intOrDie :: Value -> Either String Integer
intOrDie (VN i) = pure i
intOrDie _ = raise "type error"

-- Raise an error with message
raise :: String -> Either String a
raise = Left
