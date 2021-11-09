import {createSlice} from '@reduxjs/toolkit'

export const selectedGraphSlice = createSlice({
    name: 'selectedGraph',
    initialState: {
        graphId: "",
        graphMetadata: {},
        graphMapRef: {}
    },
    reducers: {
        graphSelected: (state, action) => {
            state.graphId = action.payload.graphId
            state.graphMetadata = action.payload.graphMetadata
        },
        graphMounted: (state, action) => {
            state.graphMapRef = action.payload.graphMapRef
        }
    }
})

export const {graphSelected, graphMounted} = selectedGraphSlice.actions

export default selectedGraphSlice.reducer