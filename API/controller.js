import { connection } from "./Data/dao.js";
import util from "util";

// promisify convierte la respuesta en promesa
// bind trae la instancia al scope local this
const query = util.promisify(connection.query).bind(connection);

const getMediciones = async (req,res) => {
    let respuesta;
    try {
        respuesta = await query(
            `SELECT * FROM medidas;`
        )
    } catch (error) {
        respuesta = error
    }
    console.log(respuesta);
    res.json(respuesta)
} 

const getUltimaMedicion = async (req, res) => {
    let respuesta;
    try {
        respuesta = await query(
            `SELECT * FROM 
            medidas ORDER BY id DESC LIMIT 1;`
        )
    } catch (error) {
        respuesta = error
    }
    console.log(respuesta);
    res.json(respuesta)
}

const crearMedicion = async (req, res) => {
    const temperatura = req.body.temperatura;
    const presion = req.body.presion;
    const humedad = req.body.humedad;
    let response
    try {
        response = await query(
            `INSERT INTO medidas(presion,temperatura,humedad) VALUES ('${presion}','${temperatura}','${humedad}')`
        )
    } catch (error) {
        response = error
    }
    res.json(response)
}

export {crearMedicion, getUltimaMedicion, getMediciones}