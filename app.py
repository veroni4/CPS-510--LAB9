import dash
from dash import Dash, html, Input, Output, callback, no_update, State
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_ag_grid as dag
import sqlite3
from pathlib import Path
import pandas as pd
import re

'''
-- NOTES REGARDING SQLITE3 -- :
1. conn = sqlite3.connect("local.db")
- Opens (or creates) the SQLite database file local.db and returns a Connection object.
- Must call conn.commit() to persist changes and conn.close() when done.

2. cur = conn.cursor()
- Creates a Cursor object bound to that Connection.
- Use cur.execute(...) to run SQL.
'''

# Function to run SQL file and return errors if any
def run_sql_file(path: str): # path is the specified sql file
    p = Path(path)
    if not p.exists():
        return [f"SQL file not found: {path}"]
    text = p.read_text(encoding="utf-8")
    # split into statements by semicolon
    parts = [s.strip() for s in re.split(r";\s*(?=\n|$)", text) if s.strip()] # split by semicolon followed by newline or end of string
    errors = [] # to collect errors
    conn = sqlite3.connect("local.db")
    cur = conn.cursor()
    for i, stmt in enumerate(parts, start=1):
        try:
            # ensure trailing semicolon for executescript
            cur.executescript(stmt + ";") # execute line by line from specified sql file (that was split into statements)
        except Exception as e:
            errors.append(f"Stmt #{i} error: {e} -- preview: {stmt[:200]!r}")
            continue
    conn.commit()
    conn.close()
    return errors

# Initialize database
def init_database():
    db_path = Path("local.db")
    # connecting will create the file if it doesn't exist
    conn = sqlite3.connect(str(db_path))
    try:
        # enable foreign key enforcement
        conn.execute("PRAGMA foreign_keys = ON;") 
        conn.commit()
    finally:
        conn.close()
    return None

# Get data from created local.db for a given table name
def get_table_data(table_name):
    try:
        conn = sqlite3.connect('local.db')
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Create dag.AgGrid for a table name (shows empty grid if df is empty)
def make_grid(table_name: str, grid_id: str = None):
    df = get_table_data(table_name)
    if df is None or (df.empty and df.columns.size == 0):
        return dag.AgGrid(
            id=grid_id,
            rowData=[],
            columnDefs=[],
            columnSize="sizeToFit",
            dashGridOptions={"rowSelection": {"mode": "multiRow"}},
            style={"height": "350px", "width": "100%"}
        )
    return dag.AgGrid(
        id=grid_id,
        rowData = df.to_dict("records"),
        columnDefs=[{"headerName": col, "field": col, "editable": True} for col in df.columns],
        columnSize="sizeToFit",
        dashGridOptions={"rowSelection": {"mode": "multiRow"}},
        style={"height": "350px", "width": "100%"})

# Initialize database
conn = init_database()

app = Dash(__name__)

# Tabs for every table
tabs_layout = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.TabsTab("Employee", leftSection=DashIconify(icon="mdi:account-outline"), value="emp"),
                dmc.TabsTab("Department", leftSection=DashIconify(icon="mingcute:department-line"), value="dep"),
                dmc.TabsTab("Leave", leftSection=DashIconify(icon="pepicons-pop:leave"), value="lev"),
                dmc.TabsTab("Payroll Record", leftSection=DashIconify(icon="mdi:file-outline"), value="p_rec"),
                dmc.TabsTab("Payroll Period", leftSection=DashIconify(icon="mingcute:time-line"), value="p_per"),
                dmc.TabsTab("Adjustment", leftSection=DashIconify(icon="material-symbols:edit-outline"), value="adj"),
            ]
        ),
        dmc.TabsPanel(html.Div(id="emp-panel"), value="emp"),
        dmc.TabsPanel(html.Div(id="dep-panel"), value="dep"),
        dmc.TabsPanel(html.Div(id="lev-panel"), value="lev"),
        dmc.TabsPanel(html.Div(id="p_rec-panel"), value="p_rec"),
        dmc.TabsPanel(html.Div(id="p_per-panel"), value="p_per"),
        dmc.TabsPanel(html.Div(id="adj-panel"), value="adj"),
    ],
    id="table-tabs", # keeps track of current table
    color="red", 
    orientation="horizontal",
    variant="default", 
    value="emp"
)
# Buttons
drop_button = dmc.Button("Drop", id="drop-button", color="red", variant="outline")
create_button = dmc.Button("Create", id="create-button", color="blue", variant="outline")
populate_button = dmc.Button("Populate", id="populate-button", color="green", variant="outline")

# Notification container (sendNotifications in callback)
notification_container = dmc.NotificationContainer(
    id="notification-container",
    sendNotifications=[]
)
# Additional buttons - After tables are created
add_row_button = dmc.Button("Add Row", id="add-row-button", color="green", variant="light", leftSection=DashIconify(icon="gridicons:add-outline"))
remove_rows_button = dmc.Button("Remove Rows", id="remove-rows-button", color="red", variant="light", leftSection=DashIconify(icon="mdi:minus-circle-outline"))
commit_button = dmc.Button("Commit Changes", id="commit-button", color="blue", variant="light",leftSection=DashIconify(icon="fluent:database-plug-connected-20-filled"))

# Main layout of the app
app.layout = dmc.MantineProvider(
        theme={"colorScheme": "light"}, 
        children=[
            html.Div(
                children=[
                    html.H1("LAB 9!"), # header
                    html.H3("Payroll Database Management Interface"), # sub-header
                    html.P("Drop all tables then create new ones and populate them",
                           style={"fontStyle": "italic", "color": "#666666", "marginTop": "0"}),
                    html.Hr(),
                    dmc.Group([drop_button, create_button, populate_button], gap="md", justify="flex-start"), # button group
                    notification_container, 
                    tabs_layout,        # tabs with tables
                    html.Div(make_grid("EMPLOYEE", "emp-grid"), style={"display": "none"}),
                    html.Div(make_grid("DEPARTMENT", "dep-grid"), style={"display": "none"}),
                    html.Div(make_grid("LEAVE", "lev-grid"), style={"display": "none"}),
                    html.Div(make_grid("PAYROLL_RECORD", "p_rec-grid"), style={"display": "none"}),
                    html.Div(make_grid("PAYROLL_PERIOD", "p_per-grid"), style={"display": "none"}),
                    html.Div(make_grid("ADJUSTMENT", "adj-grid"), style={"display": "none"}),
                    dmc.Group([add_row_button, remove_rows_button, commit_button], gap="md", justify="flex-start"), # button group
                ],
                style={"paddingLeft": "28px", "paddingRight": "28px"} 
            )
        ]
)

@app.callback(
    Output("notification-container", "sendNotifications"),
    Output("emp-panel", "children"),
    Output("dep-panel", "children"),
    Output("lev-panel", "children"),
    Output("p_rec-panel", "children"),
    Output("p_per-panel", "children"),
    Output("adj-panel", "children"),
    Input("drop-button", "n_clicks"),
    Input("create-button", "n_clicks"),
    Input("populate-button", "n_clicks"),
    Input("add-row-button", "n_clicks"),
    Input("remove-rows-button", "n_clicks"),
    Input("commit-button", "n_clicks"),
    State("table-tabs", "value"),
    State("emp-grid", "rowData"),
    State("dep-grid", "rowData"),
    State("lev-grid", "rowData"),
    State("p_rec-grid", "rowData"),
    State("p_per-grid", "rowData"),
    State("adj-grid", "rowData"),
    State("emp-grid", "selectedRows"),
    State("dep-grid", "selectedRows"),
    State("lev-grid", "selectedRows"),
    State("p_rec-grid", "selectedRows"),
    State("p_per-grid", "selectedRows"),
    State("adj-grid", "selectedRows"),
    prevent_initial_call=True
)

def handle_action(drop_n, create_n, populate_n, add_row_n, remove_n, commit_n, current_tab,
                  emp_rows, dep_rows, lev_rows, p_rec_rows, p_per_rows, adj_rows,
                  emp_selected, dep_selected, lev_selected, p_rec_selected, p_per_selected, adj_selected):
    
    triggered = dash.callback_context.triggered # triggered actions
    if not triggered:
        return no_update
    trig_id = triggered[0]["prop_id"].split(".")[0] # get the id of the triggered component

    # default notification (will be overwritten)
    notifs = []

    # Mapping tab to corresponding table name
    tab_map = {
        "emp": "EMPLOYEE",
        "dep": "DEPARTMENT",
        "lev": "LEAVE",
        "p_rec": "PAYROLL_RECORD",
        "p_per": "PAYROLL_PERIOD",
        "adj": "ADJUSTMENT",
    }
    # Mapping tab to current rowData state
    state_map = {
            "emp": emp_rows,
            "dep": dep_rows,
            "lev": lev_rows,
            "p_rec": p_rec_rows,
            "p_per": p_per_rows,
            "adj": adj_rows,
        }
    # Mapping tab to selectedRows state
    selected_map = {
            "emp": emp_selected,
            "dep": dep_selected,
            "lev": lev_selected,
            "p_rec": p_rec_selected,
            "p_per": p_per_selected,
            "adj": adj_selected,
        }
    
    def rebuild_all_from_db(): # Rebuild all grids from database
        return (
            make_grid("EMPLOYEE", "emp-grid"),
            make_grid("DEPARTMENT", "dep-grid"),
            make_grid("LEAVE", "lev-grid"),
            make_grid("PAYROLL_RECORD", "p_rec-grid"),
            make_grid("PAYROLL_PERIOD", "p_per-grid"),
            make_grid("ADJUSTMENT", "adj-grid"),
        )
    
    def panel_for(tab_key: str, table_name: str, grid_id: str, current_tab: str, rows=None, cols=None):
        """
        Return a panel child: the default make_grid(...) for non-selected tabs,
        or an AgGrid built from the provided rows/cols for the selected tab.

        rows and cols are optional and used for add-row and remove-rows
        where the client-side row list may be provided as `current_rows`.
        """
        if current_tab != tab_key:
            return make_grid(table_name, grid_id)
        # if rows not provided, pull from DB
        if rows is None:
            df = get_table_data(table_name)
            rows = df.to_dict("records") if df is not None else []

        # derive cols if not provided
        if cols is None:
            if rows and len(rows) > 0:
                cols = list(rows[0].keys())
            else:
                df = get_table_data(table_name)
                cols = list(df.columns) if df is not None else []
        col_defs = [{"headerName": c, "field": c, "editable": True} for c in cols]
        return dag.AgGrid(
            id=grid_id,
            rowData=rows,
            columnDefs=col_defs,
            columnSize="sizeToFit",
            dashGridOptions={"rowSelection": {"mode": "multiRow"}},
            style={"height": "350px", "width": "100%"}
    )
    # Drop button selected
    if trig_id == "drop-button":
        errs = run_sql_file("drop.sql")
        if errs:
            notifs = [dict(
                id="drop-notif-error",
                action="show",
                title="Drop completed with errors",
                message="; ".join(errs),
                color="red",
                icon=DashIconify(icon="mdi:alert-circle-outline"),
            )]
        else:
            notifs = [dict(
                id="drop-notif-success",
                action="show",
                title="Tables dropped",
                message="All tables were dropped successfully.",
                color="green",
                icon=DashIconify(icon="mdi:check-circle-outline"),
            )]
        emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child = rebuild_all_from_db()

    # Create button selected
    elif trig_id == "create-button":
        errs = run_sql_file("create.sql")
        if errs:
            notifs = [dict(
                id="create-notif-error",
                action="show",
                title="Create completed with errors",
                message="; ".join(errs),
                color="red",
                icon=DashIconify(icon="mdi:alert-circle-outline"),
            )]
        else:
            notifs = [dict(
                id="create-notif-success",
                action="show",
                title="Tables created",
                message="Tables were created (empty).",
                color="green",
                icon=DashIconify(icon="mdi:check-circle-outline"),
            )]
        emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child = rebuild_all_from_db()

    # Populate button selected
    elif trig_id == "populate-button":
        errs = run_sql_file("populate.sql")
        if errs:
            notifs = [dict(
                id="populate-notif-error",
                action="show",
                title="Populate completed with errors",
                message="; ".join(errs),
                color="red",
                icon=DashIconify(icon="mdi:alert-circle-outline"),
            )]
        else:
            notifs = [dict(
                id="populate-notif-success",
                action="show",
                title="Tables populated",
                message="All tables were populated successfully.",
                color="green",
                icon=DashIconify(icon="mdi:check-circle-outline"),
            )]
        emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child = rebuild_all_from_db()
    
    # Add row button selected
    elif trig_id == "add-row-button":
        # Determine which table/grid is selected
        table = tab_map.get(current_tab)
        if table is None:
            return no_update

        current_rows = state_map.get(current_tab)
        # If no user-side rowData, pull from DB to get columns (user didnt enter anything)
        if not current_rows:
            df = get_table_data(table)
            cols = list(df.columns) if df is not None else []
            current_rows = df.to_dict("records") if df is not None else []
        else:
            cols = list(current_rows[0].keys()) if len(current_rows) > 0 else []
            if not cols:
                df = get_table_data(table)
                cols = list(df.columns) if df is not None else []

        # create empty row to add to table
        empty_row = {c: None for c in cols} if cols else {}
        current_rows = list(current_rows)  # ensure mutable
        current_rows.append(empty_row)

        notifs = [dict(
            id="addrow-notif",
            action="show",
            title="Row added",
            message=f"An empty row was appended to {table}. Commit to persist.",
            color="green",
            icon=DashIconify(icon="mdi:plus-circle-outline"),
        )]
        # Build all panels: replace only the selected one with the client-side updated data
        emp_child = panel_for("emp", "EMPLOYEE", "emp-grid", current_tab, current_rows, cols)
        dep_child = panel_for("dep", "DEPARTMENT", "dep-grid", current_tab, current_rows, cols)
        lev_child = panel_for("lev", "LEAVE", "lev-grid", current_tab, current_rows, cols)
        p_rec_child = panel_for("p_rec", "PAYROLL_RECORD", "p_rec-grid", current_tab, current_rows, cols)
        p_per_child = panel_for("p_per", "PAYROLL_PERIOD", "p_per-grid", current_tab, current_rows, cols)
        adj_child = panel_for("adj", "ADJUSTMENT", "adj-grid", current_tab, current_rows, cols)

    # Remove rows button selected
    elif trig_id == "remove-rows-button":
        table = tab_map.get(current_tab)
        if table is None:
            return no_update

        current_rows = state_map.get(current_tab) or []
        selected_rows = selected_map.get(current_tab) or []

        if not selected_rows:
            notifs = [dict(
                id="remove-none",
                action="show",
                title="No rows selected",
                message="Select one or more rows in the grid to remove.",
                color="orange",
                icon=DashIconify(icon="mdi:alert-circle-outline"),
            )]
            emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child = rebuild_all_from_db()
            return notifs, emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child

        # determine columns
        if current_rows and len(current_rows) > 0:
            cols = list(current_rows[0].keys())
        else:
            df = get_table_data(table)
            cols = list(df.columns) if df is not None else []
            current_rows = df.to_dict("records") if df is not None else []

        # create a set of tuples for selected rows for robust comparison
        sel_tuples = set(tuple(s.get(c) for c in cols) for s in selected_rows)
        # filter out rows that match any selected tuple
        new_rows = [r for r in current_rows if tuple(r.get(c) for c in cols) not in sel_tuples]

        notifs = [dict(
            id="remove-success",
            action="show",
            title="Rows removed (client-side)",
            message=f"{len(current_rows) - len(new_rows)} row(s) removed from {table}. Commit to persist.",
            color="green",
            icon=DashIconify(icon="mdi:trash-can-outline"),
        )]
        emp_child = panel_for("emp", "EMPLOYEE", "emp-grid", current_tab, new_rows, cols)
        dep_child = panel_for("dep", "DEPARTMENT", "dep-grid", current_tab, new_rows, cols)
        lev_child = panel_for("lev", "LEAVE", "lev-grid", current_tab, new_rows, cols)
        p_rec_child = panel_for("p_rec", "PAYROLL_RECORD", "p_rec-grid", current_tab, new_rows, cols)
        p_per_child = panel_for("p_per", "PAYROLL_PERIOD", "p_per-grid", current_tab, new_rows, cols)
        adj_child = panel_for("adj", "ADJUSTMENT", "adj-grid", current_tab, new_rows, cols)

    # Commit button selected
    elif trig_id == "commit-button":
        table = tab_map.get(current_tab)
        if table is None:
            return no_update
        
        rows_to_commit = state_map.get(current_tab)
        if not rows_to_commit:
            notifs = [dict(
                id="commit-empty",
                action="show",
                title="Nothing to commit",
                message="No rows present in the selected grid to commit.",
                color="orange",
                icon=DashIconify(icon="mdi:alert-circle-outline"),
            )]
            emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child = rebuild_all_from_db()
            return notifs, emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child

        # Determine columns to commit
        cols = list(rows_to_commit[0].keys()) if len(rows_to_commit) > 0 else []
        errors = []
        try:
            conn = sqlite3.connect("local.db")
            cur = conn.cursor()
            #cur.execute("PRAGMA foreign_keys = ON;")
            # Clear table
            cur.execute(f"DELETE FROM {table};")
            if cols:
                placeholders = ", ".join(["?"] * len(cols))
                col_list_sql = ", ".join([f'"{c}"' for c in cols])
                insert_sql = f"INSERT INTO {table} ({col_list_sql}) VALUES ({placeholders});"
                for r in rows_to_commit:
                    vals = [r.get(c) for c in cols]
                    try:
                        cur.execute(insert_sql, vals)
                    except Exception as e:
                        errors.append(str(e))
            conn.commit()
        except Exception as e:
            errors.append(str(e))
        finally:
            conn.close()

        if errors:
            notifs = [dict(
                id="commit-error",
                action="show",
                title="Commit completed with errors",
                message="; ".join(errors),
                color="red",
                icon=DashIconify(icon="mdi:alert-circle-outline"),
            )]
        else:
            notifs = [dict(
                id="commit-success",
                action="show",
                title="Commit successful",
                message=f"Changes to {table} have been persisted.",
                color="green",
                icon=DashIconify(icon="mdi:check-circle-outline"),
            )]
        emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child = rebuild_all_from_db()

    else:
        return no_update

    return notifs, emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child

if __name__ == '__main__':
    app.run(debug=True)