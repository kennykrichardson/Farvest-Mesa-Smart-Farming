export type Crop = {
  id: number
  x: number
  y: number
  stage: string
  growth: number
  health: number
  water: number
  alive: boolean
  age: number
  ready: boolean
}

export type Farmer = {
  id: number
  x: number
  y: number
  energy: number
  task: string
  target: number | null
  steps: number
  harvests: number
  efficiency: number
}

export type HistoryPoint = {
  day: number
  growth: number
  water: number
  health: number
}

export type Snapshot = {
  meta: {
    name: string
    version: string
    day: number
    running: boolean
    width: number
    height: number
    seed: number
  }
  weather: {
    name: string
    temperature: number
    rainy: boolean
  }
  metrics: {
    total_crops: number
    living_crops: number
    dead_crops: number
    ready_crops: number
    stressed_crops: number
    farmers: number
    health: number
    water: number
    growth: number
    water_used: number
    irrigations: number
    harvests: number
    farm_score: number
  }
  crops: Crop[]
  farmers: Farmer[]
  events: { tick: number; title: string; message: string }[]
  history: HistoryPoint[]
  systems: {
    irrigation_enabled: boolean
  }
}
