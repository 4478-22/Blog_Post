import { useEffect, useRef } from "react";

type Props = {
  hasMore: boolean;
  loading: boolean;
  onLoadMore: () => void;
};

export default function useInfiniteScroll({ hasMore, loading, onLoadMore }: Props) {
  const observer = useRef<IntersectionObserver | null>(null);
  const lastElementRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (loading) return;
    if (observer.current) observer.current.disconnect();

    observer.current = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && hasMore) {
        onLoadMore();
      }
    });

    if (lastElementRef.current) {
      observer.current.observe(lastElementRef.current);
    }

    return () => {
      if (observer.current) observer.current.disconnect();
    };
  }, [loading, hasMore, onLoadMore]);

  return { lastElementRef };
}
