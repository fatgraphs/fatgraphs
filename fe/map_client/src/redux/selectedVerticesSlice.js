import {createAsyncThunk, createSlice} from '@reduxjs/toolkit'
import {fetchClosestPoint, fetchMatchingVertices} from "../APILayer";
import _ from "underscore";
import {toMapCoordinate} from "../utils/CoordinatesUtil";


export const fetchVertices = createAsyncThunk(
    'vertices/fetch',
    async (argObj, thunkAPI) => {


        function convertToMarker(groupedByEth, vertex, graphConfiguration) {
            const types = [...new Set(groupedByEth[vertex].map(obj => obj.types).flat())]
            const labels = [...new Set(groupedByEth[vertex].map(obj => obj.labels).flat())]
            const {pos, size} = groupedByEth[vertex][0]
            const mapCoordinate = toMapCoordinate(pos, graphConfiguration)

            return {
                types: types,
                labels: labels,
                pos: mapCoordinate,
                size: size,
                vertex: vertex
            }
        }

        let graphConfiguration = thunkAPI.getState().graph.graphConfiguration;
        let graphId = thunkAPI.getState().graph.graph.id;

        let verticesMatchingMetadata = await fetchMatchingVertices(graphId, argObj.metadataObject)

        // the same eth may have multiple types and labels
        let groupedByEth = _.groupBy(verticesMatchingMetadata, 'vertex');

        console.log("groupedByEth ", groupedByEth)

        let markers = []
        for (const vertex in groupedByEth) {
            markers.push(convertToMarker(groupedByEth, vertex, graphConfiguration));
        }
        markers.forEach(v => v['fetchEdges'] = argObj.fetchEdges)
        markers.forEach(v => v['flyTo'] = argObj.flyTo)
        markers.forEach(v => v['persistOnNewClick'] = argObj.persistOnNewClick)
        return markers
    }
)

export const fetchClosestVertex = createAsyncThunk(
    'vertices/fetchClosest',
    async (argObj, thunkAPI) => {
        const response = await fetchClosestPoint(argObj.graphId, argObj.pos)

        response['persistOnNewClick'] = thunkAPI.getState().marker.isPersistClick
        response['pos'] = toMapCoordinate(response["pos"], argObj.graphConfiguration)
        response['fetchEdges'] = true
        response['flyTo'] = argObj.flyTo

        return response
    }
)

export const selectedVerticesSlice = createSlice({
    name: 'markers',
    initialState: {
        isPersistClick: false,
        clearSignal: 0,
        vertices: []
    },
    reducers: {
        togglePersistClick: state => {
            state.isPersistClick = !state.isPersistClick;
        },
        clear: state => {
            state.vertices = []
            state.clearSignal += 1
        },
        pop: state => {
            state.vertices = state.vertices.slice(0, state.vertices.length - 1)
        },
        removeVertices: (state, action) => {
            state.vertices = state.vertices.filter(e => !e.types.includes(action.payload.type) || action.payload.type === undefined)
            state.vertices = state.vertices.filter(e => !e.labels.includes(action.payload.label) || action.payload.label === undefined)
            state.vertices = state.vertices.filter(e => !e.vertex === action.payload.vertex || action.payload.vertex === undefined)
            state.vertices = state.vertices.filter(e => e.persistOnNewClick || action.payload.persistOnNewClick === undefined)
        },
        updatePersistOnNewClick: (state, action) => {
            state.vertices = state.vertices.map(v => {
                if (v.vertex === action.payload.vertex) {
                    v['persistOnNewClick'] = action.payload.isChecked
                }
                return v
            })
        },
        updateFlyTo: (state, action) => {
            state.vertices[state.vertices.length - 1]['flyTo'] = false;
        }

    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchVertices.fulfilled, (state, action) => {
                state.vertices.push(...action.payload)
            })
            .addCase(fetchClosestVertex.fulfilled, (state, action) => {
                // console.log("fetchClosestVertex.fulfilled in marker slice")
                state.vertices.push(action.payload)
            })
    },
})

export const {togglePersistClick, clear, pop, removeVertices, updatePersistOnNewClick, updateFlyTo} = selectedVerticesSlice.actions

export default selectedVerticesSlice.reducer