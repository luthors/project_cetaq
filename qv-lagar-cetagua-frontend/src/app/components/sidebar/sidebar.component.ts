import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/core/services/authentication.service';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import {TooltipPosition} from '@angular/material/tooltip';
import {FormControl} from '@angular/forms';
import { EXPLOITATION_GRANADA_ID, environment } from 'src/environments/environment';


@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent {
  opened  = false;
  isSmallScreen : Boolean = false;
  showAssigModule : Boolean = true;

  positionOptions: TooltipPosition[] = ['after', 'before', 'above', 'below', 'left', 'right'];
  position = new FormControl(this.positionOptions[0]);

  constructor(private authService: AuthenticationService,
              private router: Router, private breakpointObserver: BreakpointObserver ){}

  ngOnInit() {
    this.breakpointObserver.observe([Breakpoints.Small, Breakpoints.XSmall])
      .subscribe(result => {
        this.isSmallScreen = result.matches;
      });
    
      this.showAssigModule = ( localStorage.getItem('exploitation') === EXPLOITATION_GRANADA_ID)
  }   

  logout(): void {
    this.authService.logout().subscribe(
      data => {
        this.router.navigate(['/login']);
      },
      error =>{
        console.log(error)
      }
    )
  }
}
