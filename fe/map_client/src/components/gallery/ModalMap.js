import React, {Component} from 'react';

class Modal extends Component {
    constructor(props) {
        super(props);
        console.log(props)
        this.state = {
            close_modal: props.close_modal,
            title: props.title
        }
    }

    render() {
        console.log(this.state.close_modal)
        return (
            <>
                <div
                    className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none"
                >
                    <div className="relative w-auto my-6 mx-auto">
                        {/*content*/}
                        <div
                            className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                            {/*header*/}
                            <div
                                className="flex items-start justify-between p-5 border-b border-solid border-blueGray-200 rounded-t">
                                <h3 className="text-3xl font-semibold">
                                    {this.state.title}
                                </h3>
                            </div>
                            {/*body*/}
                            <div className="relative p-6 flex-auto">
                                {this.props.children}
                            </div>
                            {/*footer*/}
                            <div
                                className="flex items-center justify-end p-6 border-t border-solid border-blueGray-200 rounded-b">
                                <button
                                    className="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                                    type="button"
                                    onClick={this.state.close_modal}
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                {/*  Background that highlights the modal and blurs what's behind it*/}
                <div className="opacity-25 fixed inset-0 z-40 bg-black"></div>
            </>
        );
    }

}

export default Modal;