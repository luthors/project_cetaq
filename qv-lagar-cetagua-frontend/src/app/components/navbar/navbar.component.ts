import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/core/services/authentication.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent {
  user: any;
  constructor(private router: Router, private authService: AuthenticationService) {
    this.user = this.authService.getCurrentUser();
  }

  navigateToProfile() {
    this.router.navigate(['/user-profile']);
  }

}


