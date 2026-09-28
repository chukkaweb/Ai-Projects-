import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function nonEmptyStringValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;
    if (typeof value !== 'string' || value.trim().length === 0) {
      return { nonEmptyString: true };
    }
    return null;
  };
}
