import express from "express";
import { config } from "dotenv";
import { crearMedicion, getMediciones, getUltimaMedicion } from "./controller.js";
import cors from 'cors'
config()

const PORT = process.env.SERVER_PORT

const app = express()

/**
 * Middlewares
 * express.json() para arreglar el body en la peticion http
 */
// app.use(express.json())
app.use(cors())
app.use(express.json())

/**
 * Obtenemos todas las mediciones
 */
app.route('/medicion').get(getMediciones)

/**
 * Creamos la medicion.
 */
app.route('/medicion').post(crearMedicion)

/**
 * Obtenemos la ultima medicion
 */
app.route('/ultima-medicion').get(getUltimaMedicion)

app.listen(PORT, ()=>{
    console.log(`el servidor se inicio en el puerto ${PORT}`);
})