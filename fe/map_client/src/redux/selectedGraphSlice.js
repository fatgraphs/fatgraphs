import {createSlice} from '@reduxjs/toolkit'

export const selectedGraphSlice = createSlice({
    name: 'selectedGraph',
    initialState: {
        graphId: "",
        graph: {},
        graphConfiguration: {},
        graphMapRef: {}
    },
    reducers: {
        graphSelected: (state, action) => {
            state.graphId = action.payload.graphId
            state.graphConfiguration = action.payload.graphConfiguration
            state.graph = action.payload.graph
        },
        graphMounted: (state, action) => {
            state.graphMapRef = action.payload.graphMapRef
        }
    }
})

export const {graphSelected, graphMounted} = selectedGraphSlice.actions

export default selectedGraphSlice.reducer