import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { FileUploadComponent } from 'src/app/components/file.upload/file.upload.component';
import { CustomerInformationService } from 'src/app/core/services/customer-information.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { ASSIGN_FILE_NAME, environment } from 'src/environments/environment';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-customer-information',
  templateUrl: './customer-information.component.html',
  styleUrls: ['./customer-information.component.scss'],
})
export class CustomerInformationComponent {
  fileAccept = false;
  clientFile= false;
  sectorFile = false;
  connectionsFile = false;
  files1: File | null = null;
  files2: File | null = null;
  files3: File | null = null;

  constructor(private matDialog: MatDialog, private customerService: CustomerInformationService, private loaderService: LoaderService){}

  onClickClient() {
    this.onClick('Clientes', ['.xlsx']);
  }

  onClickSector() {
    this.onClick('Sectores', ['.geojson']);
  }

  onClickConnections() {
    this.onClick('Acometidas', ['.geojson']);
  }

  onClick(requiredFileName: string, allowedExtensions: string[]): void {
    const dialogRef = this.matDialog.open(FileUploadComponent, {
      width: '800px',
      height: '400px',
      data: {
        title: 'Cargar fichero',
        description: this.generateDescription(requiredFileName),
        allowedExtensions: allowedExtensions,
        minFiles: 1,
        maxFiles: 1,
        validateName: true,
        optional: false,
        requiredNames: [requiredFileName],
      },
    });

    dialogRef.componentInstance.filesLoaded.subscribe((file: File) => {
      switch (requiredFileName) {
        case 'Clientes':
          this.files1 = file;
          break;
        case 'Sectores':
          this.files2 = file;
          break;
        case 'Acometidas':
          this.files3 = file;
          break;
        default:
          break;
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      switch (requiredFileName) {
        case 'Clientes':
          this.clientFile = result === 'success';
          break;
        case 'Sectores':
          this.sectorFile = result === 'success';
          break;
        case 'Acometidas':
          this.connectionsFile = result === 'success';
          break;
        default:
          break;
      }
      this.fileAccept = this.clientFile && this.connectionsFile && this.sectorFile;
    });
  }

  private generateDescription(requiredFileName: string): string {
    switch (requiredFileName) {
      case 'Clientes':
        return 'Datos de clientes. El fichero se debe llamar Clientes.xlsx';
      case 'Sectores':
        return 'Datos de sectores. El fichero se debe llamar Sectores.geojson';
      case 'Acometidas':
        return 'Datos de acometidas. El archivo se debe llamar Acometidas.geojson';
      default:
        return '';
    }
  }
  
  calculateAssigments(){
    this.loaderService.showLoader();
    if (this.files1 && this.files2 && this.files3){
      this.customerService.uploadFiles(this.files1, this.files2, this.files3)
      .subscribe(
        response => {
          this.loaderService.hideLoader();
          this.download(response);
        },
          error => {
            this.loaderService.hideLoader();
            const errorMessage = error.error.Error; 
                if (error.status === 400) {
                  // Handle specific validation errors
                  Swal.fire(
                    'Error',
                    'El fichero no tiene la estructura esperada. Por favor, descargue de nuevo el fichero de la fuente e inténtelo de nuevo',
                    'error'
                  );
                } else if (error.status === 415) {
                  const errorMessage = error.error.Error; 
                  Swal.fire(
                    'Error',
                    'Los archivos de entrada no tienen el formato correcto.<br><br>ErrorSystem' + errorMessage,
                    'error'
                  );
                } else if (error.status === 401) {
                  Swal.fire('Error', 'Error en la autenticación del usuario', 'error');
                } else if (error.status === 404) {
                  Swal.fire('Error', 'No se encuentra', 'error');
                } else {
                  Swal.fire(
                    'Error',
                    'Hubo un problema al cargar los archivos.<br><br>ErrorSystem',
                    'error'
                  );
                }
            console.error('Error al enviar los archivos al backend', error);
          }
      );
    }else {
    console.error('No se pueden cargar los archivos porque al menos uno de ellos esta vacio');
  }
    
  }

  download(response:any) {
    this.customerService.downloadFile().subscribe(
      blob => {
      const a = document.createElement('a');
      const objectUrl = URL.createObjectURL(blob);
      a.href = objectUrl;
      a.download = ASSIGN_FILE_NAME; 
      a.click();
      URL.revokeObjectURL(objectUrl);
      //Table for show the values of the percentage file
      let messageHTML = "<p> Porcentajes generados</p><table>";
      for (const [key, value] of Object.entries(response.percentajes)) {
          messageHTML += "<tr><td style='text-align: left;'>" + key + ":    </td><td style='text-align: right;'>" + value + "%</td></tr>";
      }
      messageHTML += "</table>";
      Swal.fire('Descarga exitosa', 'Se ha descargado el documento ' + ASSIGN_FILE_NAME +'<br>'+ messageHTML, 'success')
    },
    error =>{
      Swal.fire('Error', 'Error en la descraga del fichero de nuevas asignaciones', 'error')
    }
    );
  }
  
}
