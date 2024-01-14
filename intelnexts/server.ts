import dotenv from 'dotenv';
import path from "path";
require('crypto').randomBytes(64).toString('hex')
const cors = require('cors');
const express = require("express");
dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;
app.use(cors());
app.use(express.json())

// La vista bajo el path /home nos servira para la subida y descarga del pdf de forma sencilla
// El manejo de usuarios no se ha implementado debido a que no se ha considerado esencial en este momento.

app.use("/home", (req: any, res:any) => {
    res.sendFile(path.join(__dirname,"/src/views/home.html"));
})
app.use(require("./src/routes"));

app.listen(PORT, () => console.log(`Servidor ejecutandose en el puerto ${PORT}`));