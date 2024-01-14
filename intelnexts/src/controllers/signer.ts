import fs from 'fs';
import { plainAddPlaceholder } from '@signpdf/placeholder-plain';
import { P12Signer } from '@signpdf/signer-p12';
import signpdf from '@signpdf/signpdf';
import path from "path";

//Se presenta la logica del firmador, se utilizo el certificado .p12 de ejemplo según la libreria

export const signPDF = async () => {
    if(fs.existsSync(path.join(__dirname,"../../uploads/toSigned.pdf"))){
        const pdfBuffer = fs.readFileSync(path.join(__dirname,"../../uploads/toSigned.pdf"));
        const certificateBuffer = fs.readFileSync(path.join(__dirname,"../../certificate.p12"));
        const signer = new P12Signer(certificateBuffer);
        const pdfWithPlaceholder = plainAddPlaceholder({
            pdfBuffer,
            reason: 'The user is declaring consent.',
            contactInfo: 'signpdf@example.com',
            name: 'John Doe',
            location: 'Free Text Str., Free World',
        });
        const signedPdf = await signpdf.sign(pdfWithPlaceholder, signer);
        const targetPath = path.join(__dirname,"../../signed/Signed.pdf");
        fs.writeFileSync(targetPath, signedPdf);
    }
};