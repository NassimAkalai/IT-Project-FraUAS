import random
import os
import graphviz
from formatter_for_copy_paste_export_to_jack3 import *
from formatter_to_xml import format_to_xml, clear_variable_declarations
from append_question_number_to_string import append_question_number_to_string

def format_list_of_lists_of_strings_nested(lists):
    """
    Formats a list of lists of strings into a nested list 
    representation: list(list('a','b','c'), list('d','e','f'))
    """
    inner = ['list(' + ', '.join(f"'{s}'" for s in lst) + ')' for lst in lists ]
    return 'list(' + ', '.join(inner) + ')'

def generate_graph_image(matrix, start_node, filename):
    """
    Generates Graphviz-Graph from adjacency matrix and saves as png
    """
    n = len(matrix)
    dot = graphviz.Digraph()

    # Graph-Standards
    dot.attr("graph", center="True", dpi="300", label="Rumor Spread Graph", labelloc="t")

    # Add nodes
    for i in range(n):
        node_name = f"node_{i}"
        label = f"{i}"
        shape = "circle"
        penwidth = "1"

        if i == start_node:
            label += "\n(Start)"
            shape = "circle"
            penwidth = "4"

        dot.node(
            node_name,
            label,
            shape=shape,
            penwidth=penwidth,
            fixedsize="true",
            width="0.75",
            height="0.75"
        )

    # Add edges
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                dot.edge(f"node_{i}", f"node_{j}", label=str(matrix[i][j]), color="black")

    # Save png
    graph_binary = dot.pipe(format="png")
    with open(filename, "wb") as f:
        f.write(graph_binary)

def generate_task_for_bfs_rumor(question_number, num_calls=30, matrix_size=5, graph_folder="graphs"):
    """
    BFS based Rumor Spread Generator with Graphviz visualization
    """
    os.makedirs(graph_folder, exist_ok=True)
    
    matrices_rows = [[] for _ in range(matrix_size)]
    start_nodes = []
    connection_order = []

    for call_index in range(num_calls):
        matrix = [[0] * matrix_size for _ in range(matrix_size)]
        for i in range(matrix_size):
            for j in range(matrix_size):
                if i != j:
                    matrix[i][j] = random.choice([0, 1])

        start = random.randint(0, matrix_size - 1)

        # BFS traversal
        WHITE, GRAY, BLACK = 1, 2, 3
        color = [WHITE] * matrix_size
        queue = []
        order = []

        color[start] = GRAY
        queue.append(start)

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
        connection_order.append([f"Person_{x}" for x in order])

        # Generate graph image
        graph_filename = os.path.join(graph_folder, f"question_{question_number}_matrix_{call_index+1}.png")
        generate_graph_image(matrix, start, graph_filename)

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
        append_question_number_to_string(question_number, 'connection_order'),
        append_question_number_to_string(question_number, 'order'),
        format_list_of_lists_of_strings_nested(connection_order)
    ))

    return result

# Call
folder_path = "C:\\Users\\akalai\\OneDrive - Drees & Sommer SE\\Desktop\\BFS_XML"
graph_folder = os.path.join(folder_path, "graphs")
clear_variable_declarations(folder_path)

num_calls = 30
question_number = 1

result = generate_task_for_bfs_rumor(question_number, num_calls, matrix_size=5, graph_folder=graph_folder)
format_to_xml(folder_path, result, question_number, num_calls)
