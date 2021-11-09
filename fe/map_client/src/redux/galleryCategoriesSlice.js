import {createAsyncThunk, createSlice} from '@reduxjs/toolkit'
import {fetchClosestPoint, fetchMatchingVertices, getGalleryCategories} from "../APILayer";
import _ from "underscore";
import {toMapCoordinate} from "../utils/CoordinatesUtil";


export const fetchCategories = createAsyncThunk(
    'categories/fetch',
    async (argObj, thunkAPI) => {
        let rr = await getGalleryCategories()
        return rr
    }
)

export const galleryCategoriesSlice = createSlice({
    name: 'categories',
    initialState: {
        categories: []
    },
    reducers: {
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchCategories.fulfilled, (state, action) => {
                state.categories.push(...action.payload)
            })
    },
})

export const {} = galleryCategoriesSlice.actions

export default galleryCategoriesSlice.reducer