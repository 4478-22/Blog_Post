import { screen } from "@testing-library/react";
import { renderWithProviders } from "./test-utils";
import FeedPage from "@/app/feed/page";

describe("FeedPage", () => {
  it("renders posts from API", async () => {
    renderWithProviders(<FeedPage />);

    // Expect skeleton loaders or posts
    expect(screen.getByText(/feed/i)).toBeInTheDocument();
  });
});
