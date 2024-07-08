/**
 * Environment Configuration
 *
 * This file contains configuration variables for different environments.
 *
 * Usage:
 *   - Import `environment` object from this file and access its properties
 *     to dynamically configure the application based on the environment.
 *   - For example: `environment.apiUrl` will provide the API URL based on the environment.
 */

// Domains
/* export const domainSettings = {
  domainApiAuth: 'https://apicetaqua.azurewebsites.net/', // uri - url -domino - api
  domainBackend: 'https://backendcetaqua.azurewebsites.net/', // uri - url -domino - backend
  domainFrontend: 'https://cetaqua.azurewebsites.net/',
};
 */
export const domainSettings = {
  domainApiAuth: 'http://127.0.0.1:8001/', // uri - url -domino - api
  domainBackend: 'http://127.0.0.1:8000/', // uri - url -domino - backend
  domainFrontend: 'https://cetaqua.azurewebsites.net/',
};

//System URL
export const environment = {
  production: false,
  urlCustomer: domainSettings.domainApiAuth + 'api/sectors_match/', // Customer assigments module url
  urlAnomaly: domainSettings.domainApiAuth + 'api/leaks_search/', // Leak or defects search module url
  urlHydraulicPerformance:
    domainSettings.domainApiAuth + 'api/hydraulic_performance/', // Hydraulic performanse module url
  loginUrl: domainSettings.domainApiAuth + 'login/',
  logoutUrl: domainSettings.domainApiAuth + 'logout/',
  updateProfileUrl : domainSettings.domainApiAuth + 'users/',
  downloadMatch: domainSettings.domainApiAuth + 'file/store/file/output.csv',
  resetUrl: domainSettings.domainApiAuth + 'reset_password/',

  saveVariablesUrl: domainSettings.domainBackend + 'api/anomaly_filter/',
  getVariablesUrl: domainSettings.domainBackend + 'api/indicator_threshold/',
  helpInformationurl:
    domainSettings.domainFrontend + 'assets/json/help-info.json',
  helpInfovariablesurl:
    domainSettings.domainFrontend + 'assets/json/help-variables.json',
  performanceHistoryUrl:
    domainSettings.domainBackend + 'api/hydraulic_performance/',
  listThresholdUrl: domainSettings.domainBackend + 'api/indicator_threshold/',
  listMapUrl: domainSettings.domainBackend + 'api/map/',
  exploitationUrl: domainSettings.domainBackend + 'api/exploitation/',

  manualUserUrl: domainSettings.domainFrontend + 'assets/files/Manual.pdf', //Manual url

};

// Constants for the anomaly filter. Default values for created the formGroup
export const MAX_NUMBER_OF_DAYS = 7;
export const DEFAULT_CONSECUTIVE_DAYS = 2;
export const DEFAULT_INDICATOR_NUMBER = 3;

// Constants for the match module
export const MANUAL_NAME = 'Manual.pdf'; // Name for the user manual  download
export const ASSIGN_FILE_NAME = 'Nueva asignación'; // Name for the new assigment download

// Constant for especific exploitation
export const EXPLOITATION_GRANADA_ID = '2';

//Constant for the limit of items on the hydraulic performance graph
export const MAX_ITEMS_GRAPH = 24;
