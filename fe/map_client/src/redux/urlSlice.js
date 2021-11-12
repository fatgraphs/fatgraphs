import {createSlice} from '@reduxjs/toolkit'
import {fetchClosestVertex} from "./selectedVerticesSlice";

export const urlSlice = createSlice({
    name: 'url',
    initialState: {
        x: - 128,
        y: 128,
        z: 0,
        vertex: ''
    },
    reducers: {
        changeUrl: (state, action) => {
            console.log("changeUrl ", action.payload)
            state.x = action.payload.x || state.x
            state.y = action.payload.y || state.y
            if(action.payload.z !== undefined){
                state.z = action.payload.z
            }
            state.vertex = action.payload.vertex || state.vertex
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchClosestVertex.fulfilled, (state, action) => {
                state.vertex = action.payload.vertex
            })
    },
})

export const {changeUrl} = urlSlice.actions

export default urlSlice.reducer