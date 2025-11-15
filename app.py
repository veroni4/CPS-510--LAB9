import dash
from dash import Dash, html, Input, Output, callback, no_update
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
def make_grid(table_name: str):
    df = get_table_data(table_name)
    if df is None:
        return html.Div(f"{table_name} not found")
    # if no columns, show a message
    if df.empty and df.columns.size == 0:
        return html.Div(f"{table_name} not found or has no columns")
    return dag.AgGrid(
        rowData = df.to_dict("records"),
        columnDefs=[{"headerName": col, "field": col} for col in df.columns],
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

# Main layout of the app
app.layout = dmc.MantineProvider(
        theme={"colorScheme": "light"}, 
        children=[
            html.H1("LAB 9!"), # header
            dmc.Group([drop_button, create_button, populate_button], gap="md", justify="flex-start"), # button group
            notification_container, 
            tabs_layout        # tabs with tables
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
    prevent_initial_call=True
)
def handle_action(drop_n, create_n, populate_n):
    triggered = dash.callback_context.triggered # triggered actions
    if not triggered:
        return no_update
    trig_id = triggered[0]["prop_id"].split(".")[0] # get the id of the triggered component

    # default notification (will be overwritten)
    notifs = []
    # perform action
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
    else:
        return no_update

    # after action, make grids for each table
    emp_child = make_grid("EMPLOYEE")
    dep_child = make_grid("DEPARTMENT")
    lev_child = make_grid("LEAVE")
    p_rec_child = make_grid("PAYROLL_RECORD")
    p_per_child = make_grid("PAYROLL_PERIOD")
    adj_child = make_grid("ADJUSTMENT")

    return notifs, emp_child, dep_child, lev_child, p_rec_child, p_per_child, adj_child


if __name__ == '__main__':
    app.run(debug=True)