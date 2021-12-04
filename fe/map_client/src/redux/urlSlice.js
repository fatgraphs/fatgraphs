import {createSlice} from '@reduxjs/toolkit'
import {fetchClosestVertex} from "./selectedVerticesSlice";
const configs = require('configurations')

export const urlSlice = createSlice({
    name: 'url',
    initialState: {
        x: '',
        y: '',
        z: '0',
        vertex: ''
    },
    reducers: {
        changeUrl: (state, action) => {
            state.x = action.payload.x + '' || state.x + ''
            state.y = action.payload.y + '' || state.y + ''
            state.z = action.payload.z + '' || state.z + ''
            state.vertex = action.payload.vertex || state.vertex
        }
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