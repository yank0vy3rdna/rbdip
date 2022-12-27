import Dropzone, {useDropzone} from "react-dropzone";
import {useCallback, useEffect, useRef, useState} from "react";

function App() {
    const [mode, setMode] = useState("vignette")
    const [resultImage, setResultImage] = useState("")
    const ws = useRef(null);

    const onImageDrop = useCallback(acceptedFiles => {
        console.log(acceptedFiles, mode)
    }, [mode])
    useEffect(() => {
        ws.current = new WebSocket("ws://localhost:8080/ws")
        ws.current.onmessage = e => {
            const arr = new Uint8Array(e.data);
            const blob = new Blob([arr.buffer]);
            const reader = new FileReader();
            reader.onload = e => {
                setResultImage(e.target.result)
            }
            reader.readAsDataURL(blob);
        }
    }, [])
    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop: onImageDrop})
    return (
        <div style={{
            height: "100vh",
            width: "100vw",
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
        }}>
            <div>
                <select onChange={(e) => {
                    setMode(e.target.value)
                }} value={mode}>
                    <option value="vignette">vignette</option>
                    <option value="delete_faces">delete_faces</option>
                    <option value="detail">detail</option>
                    <option value="sharp">sharp</option>
                    <option value="negative">negative</option>
                    <option value="smooth">smooth</option>
                </select>
                <div style={{background: "#d2d2d2", height: "300px"}} {...getRootProps()}>
                    <input {...getInputProps()} />
                    {
                        isDragActive ?
                            <p>Drop the files here ...</p> :
                            <p>Drag 'n' drop some files here, or click to select files</p>
                    }
                </div>
                <img src={resultImage} alt={"Result image"}/>
            </div>
        </div>
    );
}

export default App;
