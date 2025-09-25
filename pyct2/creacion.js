document.getElementById("crearchivo").addEventListener("click", cosita)

function cosita(){
    let elcontenido = document.getElementById("Eltxtito").value
    let frmt = document.getElementById("frmt").value
    if(frmt === "txt"){
        const contenido = elcontenido
        const arch = new Blob([contenido], {type: 'text/plain'})
        const enlace = document.createElement('a');
        enlace.href = URL.createObjectURL(arch);
        enlace.download = 'archivo.txt';
        enlace.click();
    } else if(frmt === "pdf"){
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        const marginLeft = 10;
        const marginTop = 10;
        const lineHeight = 10;
        const pageHeight = doc.internal.pageSize.getHeight();
        const pageWidth = doc.internal.pageSize.getWidth();
        const maxLineWidth = pageWidth - marginLeft * 2;
    
        const lines = doc.splitTextToSize(elcontenido, maxLineWidth);
    
        let y = marginTop;
    
        lines.forEach((linea, i) => {
          if (y + lineHeight > pageHeight - marginTop) {
            doc.addPage();
            y = marginTop;
          }
          doc.text(linea, marginLeft, y);
          y += lineHeight;
        });

        doc.save("archivo.pdf");
    }
}

//para conectar con python:
//https://www.youtube.com/watch?v=Jp8TJcDjzVM