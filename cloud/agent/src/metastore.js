import _ from 'lodash'


export class Metastore {
    constructor(init_tables) {
        this.tables = { }
        for (var table of init_tables) {
            this.initTable(table)
        }
    }

    initTable = kind => {
        const table = new Metatable()
        this.tables[kind] = table
        return table
    }

    getTable = kind => {
        const table = this.tables[kind]
        if (!table) {
            throw new Error(`Unknown meta table ${kind}`)
        }
        return table
    }

    get = (kind, id) => {
        const table = this.getTable(kind)
        return table.get(id)
    }

    getAll = kind => {
        const table = this.getTable(kind)
        return table.getAll()
    }

    set = (kind, id, value) => {
        let table = this.tables[kind]
        if (!table) {
            table = this.initTable(kind)
        }
        return table.set(id, value)
    }

    update = (kind, id, transform) => {
        const table = this.getTable(kind)
        return table.update(id, transform)
    }

    del = (kind, id) => {
        const table = this.getTable(kind)
        table.del(id)
    }
}

export class Metatable {
    constructor() {
        this.order = [ ]
        this.items = { }
    }

    get = id => {
        let item = this.items[id]
        if (!item) {
            throw new Error(`No such item ${id}`)
        }
        return item
    }

    getAll = () => {
        return _.map(this.order, id => this.items[id])
    }

    set = (id, value) => {
        if (!_.includes(this.order, id)) {
            this.order.push(id)
        }
        this.items[id] = value
        console.log(this.items[id])
    }

    update = (id, transform) => {
        let item = this.items[id]
        if (!item) {
            throw new Error(`No such item ${id}`)
        }
        this.items[id] = transform(item)
        console.log(this.items[id])
    }

    del = id => {
        _.remove(this.order, i => i === id)
        delete this.items[id]
    }
}