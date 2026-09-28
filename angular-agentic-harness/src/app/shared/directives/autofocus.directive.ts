import { Directive, HostListener, input } from '@angular/core';

@Directive({
  selector: '[appAutofocus]',
  standalone: true,
})
export class AutofocusDirective {
  readonly appAutofocus = input(true);

  @HostListener('focus')
  onFocus(): void {
    // HostListener keeps the directive tree-shakable and testable.
  }
}
