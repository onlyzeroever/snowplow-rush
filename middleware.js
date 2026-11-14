// Login for the level editor (Vercel Routing Middleware).
// The username and password live in the Vercel project's environment variables
// EDITOR_USER and EDITOR_PASSWORD; they are never stored in this repo.
// If they aren't set, the editor stays locked.

export const config = {
  matcher: ['/editor', '/editor.html'],
};

function sameText(a, b) {
  // compare without leaking how many characters matched
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}

function locked(text) {
  return new Response(text, {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Snowplow Rush editor", charset="UTF-8"',
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
}

export default function middleware(request) {
  const user = process.env.EDITOR_USER;
  const pass = process.env.EDITOR_PASSWORD;
  if (!user || !pass) return locked('The editor login is not set up yet.');

  const auth = request.headers.get('authorization') || '';
  if (auth.startsWith('Basic ')) {
    let decoded = '';
    try { decoded = atob(auth.slice(6)); } catch (e) { decoded = ''; }
    const i = decoded.indexOf(':');
    if (i > 0 && sameText(decoded.slice(0, i), user) && sameText(decoded.slice(i + 1), pass)) {
      // carry on to the editor page (same as next() from @vercel/functions)
      return new Response(null, { headers: { 'x-middleware-next': '1' } });
    }
  }
  return locked('Login required.');
}
