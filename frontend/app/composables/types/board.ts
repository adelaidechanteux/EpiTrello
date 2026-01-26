export interface Task {
    id: string
    title: string
    description: string | null
    category: string
    color: string | null
    date_start: string | null
    date_end: string | null
    assigned: string | null
    completed: boolean
}

export interface Column {
    id: string
    title: string
    cards: Task[]
}
