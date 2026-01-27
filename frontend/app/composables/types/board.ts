export interface Task {
    id: string
    title: string
    description: string | null
    category: string
    color: string | null
    date_start: string | null
    date_end: string | null
    assigned: any
    completed: boolean
}

export interface Column {
    id: string
    title: string
    cards: Task[]
}

export interface User {
    id: string
    username: string
    email: string
    profile_picture: string
}
