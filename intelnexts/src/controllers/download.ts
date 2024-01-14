import * as path from "path";

// Retorna el archivo pdf firmado ubicado en la carpeta signed.

exports.downloadSign =(req: any, res:any) => {
    res.download(path.join(__dirname,"../../signed/Signed.pdf"));
}
