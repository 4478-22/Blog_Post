import { screen, fireEvent, waitFor } from "@testing-library/react";
import { renderWithProviders } from "./test-utils";
import LoginPage from "@/app/login/page";
import { useAuthStore } from "@/store/auth-store";
import api from "@/lib/api";

jest.mock("@/lib/api");
const mockedApi = api as jest.Mocked<typeof api>;

describe("LoginPage", () => {
  beforeEach(() => {
    useAuthStore.setState({ user: null, tokens: null });
  });

  it("logs in successfully", async () => {
    mockedApi.post.mockResolvedValueOnce({
      data: { access: "token123", refresh: "refresh123" },
    });
    mockedApi.get.mockResolvedValueOnce({
      data: { id: 1, username: "alice", email: "a@x.com" },
    });

    renderWithProviders(<LoginPage />); // ✅ wrapped in ToastProvider

    fireEvent.change(screen.getByLabelText(/Username or Email/i), {
      target: { value: "alice" },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "passw0rd" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Login/i }));

    await waitFor(() =>
      expect(useAuthStore.getState().user?.username).toBe("alice")
    );
  });
});
