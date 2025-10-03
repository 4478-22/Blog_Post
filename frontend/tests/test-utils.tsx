import { render } from "@testing-library/react";
import { ToastProvider } from "@/components/Toast";

export function renderWithProviders(ui: React.ReactElement) {
  return render(<ToastProvider>{ui}</ToastProvider>);
}
