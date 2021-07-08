import React from "react";
// React context API is similar to Redux but simpler.
// In a nutshell it allows global variables shared across all components
export const MyContext = React.createContext({autocompletion_types: [], autocompletion_labels: []});