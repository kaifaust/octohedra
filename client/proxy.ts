import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function proxy(request: NextRequest) {
  const { pathname, search } = request.nextUrl;

  // Strip query params from opengraph-image and twitter-image routes
  // Facebook and other crawlers append cache-busting params that can cause issues
  if (
    (pathname.endsWith('/opengraph-image') || pathname.endsWith('/twitter-image')) &&
    search
  ) {
    const url = request.nextUrl.clone();
    url.search = '';
    return NextResponse.redirect(url, 308);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/r/:recipe/opengraph-image',
    '/r/:recipe/twitter-image',
    '/s/:id/opengraph-image',
    '/s/:id/twitter-image',
    '/opengraph-image',
    '/twitter-image',
  ],
};
