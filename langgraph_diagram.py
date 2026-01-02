"""
LangGraph Architecture Diagram Generator

This script creates visual diagrams showing how LangGraph works, including:
- Basic graph structure (nodes and edges)
- State management flow
- Agent workflow example (Time-Off Assistant)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.lines as mlines

def create_basic_langgraph_diagram():
    """Creates a diagram showing basic LangGraph concepts"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'LangGraph Architecture Overview',
            fontsize=20, weight='bold', ha='center')

    # Define node positions
    nodes = {
        'START': (2, 7.5),
        'Agent': (5, 7.5),
        'Tools': (8, 7.5),
        'Human': (5, 5),
        'State': (2, 5),
        'END': (8, 5)
    }

    # Draw nodes
    node_colors = {
        'START': '#90EE90',
        'Agent': '#87CEEB',
        'Tools': '#FFD700',
        'Human': '#FFA07A',
        'State': '#DDA0DD',
        'END': '#F08080'
    }

    for node_name, (x, y) in nodes.items():
        if node_name in ['START', 'END']:
            circle = Circle((x, y), 0.3, color=node_colors[node_name],
                          ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, node_name, ha='center', va='center',
                   fontsize=10, weight='bold', zorder=4)
        else:
            box = FancyBboxPatch((x-0.5, y-0.3), 1, 0.6,
                                boxstyle="round,pad=0.1",
                                facecolor=node_colors[node_name],
                                edgecolor='black', linewidth=2, zorder=3)
            ax.add_patch(box)
            ax.text(x, y, node_name, ha='center', va='center',
                   fontsize=11, weight='bold', zorder=4)

    # Draw edges with arrows
    edges = [
        ('START', 'Agent', 'Input'),
        ('Agent', 'Tools', 'Tool Call'),
        ('Tools', 'Agent', 'Result'),
        ('Agent', 'Human', 'Interrupt'),
        ('Human', 'Agent', 'Response'),
        ('Agent', 'State', 'Update'),
        ('State', 'END', 'Complete')
    ]

    arrow_style = 'fancy,head_length=0.8,head_width=0.5'

    for start, end, label in edges:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]

        # Adjust arrow positions to account for node sizes
        if start in ['START', 'END']:
            x1_adj, y1_adj = x1, y1
        else:
            x1_adj, y1_adj = x1, y1

        if end in ['START', 'END']:
            x2_adj, y2_adj = x2, y2
        else:
            x2_adj, y2_adj = x2, y2

        arrow = FancyArrowPatch((x1_adj, y1_adj), (x2_adj, y2_adj),
                               arrowstyle=arrow_style, color='black',
                               linewidth=2, mutation_scale=20, zorder=2)
        ax.add_patch(arrow)

        # Add label
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.2, label, fontsize=9, ha='center',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Add key concepts box
    concepts_text = """
    Key Concepts:

    • Nodes: Functions that process state
    • Edges: Connections between nodes
    • State: Shared data across the graph
    • Tools: External functions the agent can call
    • Human-in-the-loop: Pause for human input
    """

    ax.text(0.5, 2.5, concepts_text, fontsize=10,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Add benefits box
    benefits_text = """
    Benefits of LangGraph:

    ✓ Stateful conversations
    ✓ Complex decision flows
    ✓ Human approval checkpoints
    ✓ Persistence & memory
    ✓ Cycle & loop support
    """

    ax.text(6.5, 2.5, benefits_text, fontsize=10,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    plt.tight_layout()
    return fig

def create_timeoff_workflow_diagram():
    """Creates a detailed workflow diagram for the Time-Off Assistant example"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(5, 11.5, 'Time-Off Assistant Workflow (LangGraph)',
            fontsize=20, weight='bold', ha='center')

    # Node positions
    nodes = {
        'START': (2, 10),
        'Parse Request': (5, 10),
        'Check Balance': (5, 8.5),
        'Enough Days?': (5, 7),
        'Request Info': (2, 5.5),
        'Wait Human': (2, 4),
        'Approve': (7, 5.5),
        'Deny': (7, 4),
        'Update DB': (5, 2.5),
        'END': (5, 1)
    }

    # Node colors by type
    node_colors = {
        'START': '#90EE90',
        'Parse Request': '#87CEEB',
        'Check Balance': '#87CEEB',
        'Enough Days?': '#FFD700',
        'Request Info': '#FFA07A',
        'Wait Human': '#FFA07A',
        'Approve': '#98FB98',
        'Deny': '#F08080',
        'Update DB': '#DDA0DD',
        'END': '#90EE90'
    }

    # Draw nodes
    for node_name, (x, y) in nodes.items():
        if node_name in ['START', 'END']:
            circle = Circle((x, y), 0.3, color=node_colors[node_name],
                          ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, node_name, ha='center', va='center',
                   fontsize=9, weight='bold', zorder=4)
        elif node_name == 'Enough Days?':
            # Diamond shape for decision
            from matplotlib.patches import Polygon
            diamond = Polygon([(x, y+0.4), (x+0.6, y), (x, y-0.4), (x-0.6, y)],
                            facecolor=node_colors[node_name],
                            edgecolor='black', linewidth=2, zorder=3)
            ax.add_patch(diamond)
            ax.text(x, y, node_name, ha='center', va='center',
                   fontsize=9, weight='bold', zorder=4)
        else:
            box = FancyBboxPatch((x-0.65, y-0.3), 1.3, 0.6,
                                boxstyle="round,pad=0.1",
                                facecolor=node_colors[node_name],
                                edgecolor='black', linewidth=2, zorder=3)
            ax.add_patch(box)
            ax.text(x, y, node_name, ha='center', va='center',
                   fontsize=9, weight='bold', zorder=4)

    # Draw edges
    arrow_style = 'fancy,head_length=0.6,head_width=0.4'

    edges = [
        ('START', 'Parse Request', ''),
        ('Parse Request', 'Check Balance', 'Call tool:\nget_balance()'),
        ('Check Balance', 'Enough Days?', ''),
        ('Enough Days?', 'Request Info', 'No/Missing'),
        ('Enough Days?', 'Approve', 'Yes'),
        ('Request Info', 'Wait Human', 'Interrupt'),
        ('Wait Human', 'Parse Request', 'Resume'),
        ('Approve', 'Update DB', 'approve_request()'),
        ('Deny', 'Update DB', 'deny_request()'),
        ('Enough Days?', 'Deny', 'Balance low'),
        ('Update DB', 'END', 'Persist state')
    ]

    for start, end, label in edges:
        if start not in nodes or end not in nodes:
            continue

        x1, y1 = nodes[start]
        x2, y2 = nodes[end]

        # Create curved arrows for some paths
        if (start, end) in [('Wait Human', 'Parse Request')]:
            # Curved arrow
            connectionstyle = "arc3,rad=0.3"
        else:
            connectionstyle = "arc3,rad=0"

        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle=arrow_style, color='black',
                               linewidth=2, mutation_scale=15, zorder=2,
                               connectionstyle=connectionstyle)
        ax.add_patch(arrow)

        # Add label
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.3, mid_y, label, fontsize=8, ha='left',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    # Add state management info
    state_text = """
    Graph State:

    • messages: Conversation history
    • user_id: Current user
    • balance: Available days
    • request: Parsed request details
    • status: approved/denied/pending
    """

    ax.text(0.3, 8, state_text, fontsize=9,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='#DDA0DD', alpha=0.3))

    # Add tools info
    tools_text = """
    Available Tools:

    🔧 get_balance(user_id)
    🔧 approve_request(user_id, days)
    🔧 deny_request(user_id, reason)
    🔧 parse_dates(text)
    """

    ax.text(7.5, 8, tools_text, fontsize=9,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='#FFD700', alpha=0.3))

    plt.tight_layout()
    return fig

def create_state_management_diagram():
    """Creates a diagram showing how state flows through a LangGraph"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(5, 7.5, 'LangGraph State Management Flow',
            fontsize=20, weight='bold', ha='center')

    # Show state evolution through nodes
    states = [
        (1.5, 5, "Initial State\n{'messages': []}"),
        (3.5, 5, "After User Input\n{'messages': [user_msg]}"),
        (5.5, 5, "After Agent\n{'messages': [...],\n'tool_call': {...}}"),
        (7.5, 5, "After Tool\n{'messages': [...],\n'result': {...}}"),
    ]

    for i, (x, y, text) in enumerate(states):
        # Draw state box
        box = FancyBboxPatch((x-0.6, y-0.5), 1.2, 1,
                            boxstyle="round,pad=0.1",
                            facecolor='#DDA0DD',
                            edgecolor='black', linewidth=2, zorder=3)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center',
               fontsize=8, zorder=4)

        # Draw arrow to next state
        if i < len(states) - 1:
            arrow = FancyArrowPatch((x+0.6, y), (states[i+1][0]-0.6, y),
                                   arrowstyle='->', color='black',
                                   linewidth=3, mutation_scale=20, zorder=2)
            ax.add_patch(arrow)

    # Add persistence layer
    persistence_box = FancyBboxPatch((1, 2.5), 8, 1,
                                    boxstyle="round,pad=0.1",
                                    facecolor='lightblue',
                                    edgecolor='black', linewidth=2,
                                    linestyle='--', zorder=1)
    ax.add_patch(persistence_box)
    ax.text(5, 3, 'Persistence Layer (SQLite / PostgreSQL / Memory)',
           ha='center', va='center', fontsize=11, weight='bold')

    # Add arrows showing save/load
    for x, _, _ in states:
        # Down arrow (save)
        arrow = FancyArrowPatch((x, 4.5), (x, 3.5),
                               arrowstyle='->', color='blue',
                               linewidth=2, mutation_scale=15, zorder=2,
                               linestyle='--')
        ax.add_patch(arrow)

    # Add explanation boxes
    explain_text = """
    State Update Pattern:

    1. Node receives current state
    2. Node processes and modifies state
    3. State is merged with previous state
    4. Updated state passed to next node
    5. State persisted to storage
    """

    ax.text(0.5, 0.5, explain_text, fontsize=9,
           verticalalignment='bottom',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    features_text = """
    Key Features:

    ✓ Automatic state merging
    ✓ Type-safe with TypedDict
    ✓ Reducer functions (add, replace)
    ✓ Checkpointing for resume
    ✓ Time-travel debugging
    """

    ax.text(5.5, 0.5, features_text, fontsize=9,
           verticalalignment='bottom',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    plt.tight_layout()
    return fig

def save_all_diagrams():
    """Generate and save all diagrams"""
    print("Generating LangGraph diagrams...")

    # Create images directory if it doesn't exist
    import os
    os.makedirs('images', exist_ok=True)

    # Generate diagrams
    fig1 = create_basic_langgraph_diagram()
    fig1.savefig('images/langgraph_architecture.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: images/langgraph_architecture.png")

    fig2 = create_timeoff_workflow_diagram()
    fig2.savefig('images/timeoff_workflow.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: images/timeoff_workflow.png")

    fig3 = create_state_management_diagram()
    fig3.savefig('images/state_management.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: images/state_management.png")

    print("\n✅ All diagrams generated successfully!")
    print("\nDiagrams created:")
    print("  1. langgraph_architecture.png - Overview of LangGraph concepts")
    print("  2. timeoff_workflow.png - Detailed Time-Off Assistant workflow")
    print("  3. state_management.png - How state flows through the graph")

    # Close figures to prevent display
    plt.close('all')

if __name__ == "__main__":
    save_all_diagrams()
