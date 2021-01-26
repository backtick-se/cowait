Module cowait.tasks.agent.tasklist
==================================

Classes
-------

`TaskList(task)`
:   In-memory database containing all seen tasks and logs

    ### Ancestors (in MRO)

    * builtins.dict

    ### Methods

    `on_fail(self, conn: cowait.network.conn.Conn, id, error, **msg)`
    :

    `on_init(self, conn: cowait.network.conn.Conn, id: str, task: dict, **msg)`
    :

    `on_log(self, conn: cowait.network.conn.Conn, id, file, data, **msg)`
    :

    `on_return(self, conn: cowait.network.conn.Conn, id, result, **msg)`
    :

    `on_status(self, conn: cowait.network.conn.Conn, id, status, **msg)`
    :