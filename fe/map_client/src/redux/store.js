import {configureStore} from '@reduxjs/toolkit'
import markersSlice from "./selectedVerticesSlice";
import urlSlice from "./urlSlice";
import selectedGraphSlice from "./selectedGraphSlice";
import galleryCategoriesSlice from "./galleryCategoriesSlice";

export default configureStore({
    reducer: {
        marker: markersSlice,
        url: urlSlice,
        graph: selectedGraphSlice,
        categories: galleryCategoriesSlice
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware({
        serializableCheck: false
    }),
})