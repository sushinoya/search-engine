from collections import defaultdict

# Shunting-yard

operators = op_not, op_and, op_or = "NOT", "AND", "OR"
parens = left_par, right_par = "(", ")"
normalisation_rules = {token: " {} ".format(token) for token in parens}
precedence = defaultdict(lambda: -1, {
    op_not: 0,
    op_and: 0,
    op_or: 0
})


def tokenize(formula):
    for find, replace in normalisation_rules.items():
        formula = formula.replace(find, replace)
    return formula.split()


def is_operand(token):
    return not is_operator(token) and token not in parens


def is_operator(token):
    return token in operators


def not_greater_precedence(token, top_stack_item):
    return precedence[token] <= precedence[top_stack_item]


def shunting_yard(infix):
    tokens = tokenize(infix)
    output = []
    op_stack = []

    for token in tokens:
        if is_operand(token):
            output.append(token)

        elif token is left_par:
            op_stack.append(token)

        elif token is right_par:
            while op_stack and op_stack[-1] is not left_par:
                stack_token = op_stack.pop()
                output.append(stack_token)
            op_stack.pop()  # Removing the "("

        else:
            while op_stack and not_greater_precedence(token, op_stack[-1]):
                output.append(op_stack.pop())
            op_stack.append(token)

    if op_stack:
        output.extend(reversed(op_stack))
    return ' '.join(output)
