import {createSlice} from '@reduxjs/toolkit'
import {fetchClosestVertex} from "./selectedVerticesSlice";
const configs = require('configurations')

export const urlSlice = createSlice({
    name: 'url',
    initialState: {
        x: String(configs['tile_size'] / -2),
        y: String(configs['tile_size'] / 2),
        z: '0',
        vertex: ''
    },
    reducers: {
        changeUrl: (state, action) => {
            state.x = action.payload.x + '' || state.x + ''
            state.y = action.payload.y + '' || state.y + ''
            state.z = action.payload.z + '' || state.z + ''
            state.vertex = action.payload.vertex || state.vertex
        },
        resetUrl: (state, action) => {
            state.x = String(configs['tile_size'] / -2)
            state.y = String(configs['tile_size'] / 2)
            state.z = '0'
            state.vertex = ''
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchClosestVertex.fulfilled, (state, action) => {
                // when the redux store fetches the closest vertex to where user has clicked,
                // it's saved here to be shown in the browser url
                state.vertex = action.payload.vertex
            })
    },
})

export const {changeUrl, resetUrl} = urlSlice.actions

export default urlSlice.reducer