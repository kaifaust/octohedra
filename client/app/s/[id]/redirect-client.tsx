'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface RedirectClientProps {
  to: string;
}

export function RedirectClient({ to }: RedirectClientProps) {
  const router = useRouter();

  useEffect(() => {
    router.replace(to);
  }, [router, to]);

  return null;
}
