import random
from formatter_for_copy_paste_export_to_jack3 import *
from formatter_to_xml import format_to_xml, clear_variable_declarations
from append_question_number_to_string import append_question_number_to_string

def format_list_of_lists_of_strings_nested(lists):
    """
    New function for nested lists
    Formats a list of lists of strings into a nested list 
    representation: list(list('a','b','c'), list('d','e','f'))
    """
    inner = [ 'list(' + ', '.join(f"'{s}'" for s in lst) + ')' for lst in lists ]
    return 'list(' + ', '.join(inner) + ')'

# BFS based Virus Spread Generator with separate rows to work with jack
def generate_task_for_bfs_virus(question_number, num_calls = 30, matrix_size = 5):
    matrices_rows = [[] for _ in range(matrix_size)]
    start_nodes = []
    infection_order = []

    # Random adjacency matrix
    for _ in range(num_calls):
        matrix = [[0] * matrix_size for _ in range(matrix_size)]
        for i in range(matrix_size):
            for j in range(matrix_size):
                if i != j:
                    matrix[i][j] = random.choice([0, 1])

        start = random.randint(0, matrix_size - 1)

        # BFS based on Prof. Liebehenschel's code but slightly shortened
        WHITE, GRAY, BLACK = 1, 2, 3
        color = [WHITE] * matrix_size
        queue = []
        order = []

        color[start] = GRAY
        queue.append(start)

        # BFS traversal
        while queue:
            node = queue.pop(0)
            order.append(node)
            for succ in range(matrix_size):
                if matrix[node][succ] > 0 and color[succ] == WHITE:
                    color[succ] = GRAY
                    queue.append(succ)
            color[node] = BLACK

        # Save rows
        for i in range(matrix_size):
            matrices_rows[i].append(matrix[i])

        start_nodes.append(start)

        # Person formatting here
        infection_order.append([f"Person_{x}" for x in order])

    # XML formatting
    result = []

    for i in range(matrix_size):
        row_list_name = append_question_number_to_string(question_number, f'matrix_rows_{i+1}')
        single_row_name = append_question_number_to_string(question_number, f'matrix_row_{i+1}_single')
        result.append((
            row_list_name,
            single_row_name,
            format_list_of_arrays(matrices_rows[i])
        ))

    result.append((
        append_question_number_to_string(question_number, 'start_nodes'),
        append_question_number_to_string(question_number, 'start_node'),
        format_list_of_integers(start_nodes)
    ))

    result.append((
        append_question_number_to_string(question_number, 'infection_order'),
        append_question_number_to_string(question_number, 'order'),
        format_list_of_lists_of_strings_nested(infection_order)
    ))

    return result
    
# Call
folder_path = "YOUR_PATHWAY_HERE"
clear_variable_declarations(folder_path)

num_calls = 30
question_number = 1

result = generate_task_for_bfs_virus(question_number, num_calls, matrix_size = 5)

format_to_xml(folder_path, result, question_number, num_calls)
