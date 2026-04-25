const Markdoc = require('@markdoc/markdoc');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const tags = require('./markdoc/tags');
const i18nData = require('./i18n/dynamic');

// Parse CLI args
const args = process.argv.slice(2);
let base = '/bergen-paris-weather';
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--base' && i + 1 < args.length) {
    base = args[i + 1];
    i++;
  }
}
// Normalize base: empty string means root
if (base === '') {
  base = '';
} else {
  if (!base.startsWith('/')) base = '/' + base;
  if (base.endsWith('/') && base.length > 1) base = base.slice(0, -1);
}

const pages = [
  { content: 'content/en/index.md', template: 'templates/index.html', output: 'dist/en/index.html', lang: 'en' },
  { content: 'content/fr/index.md', template: 'templates/index.html', output: 'dist/fr/index.html', lang: 'fr' },
  { content: 'content/en/about.md', template: 'templates/about.html', output: 'dist/en/about.html', lang: 'en' },
  { content: 'content/fr/about.md', template: 'templates/about.html', output: 'dist/fr/about.html', lang: 'fr' },
];

// dist_text functions for EN and FR — embedded in I18N JSON
const distTextEn = `function(name, km, tKm, pKm, pToC) {
  var tMins = Math.round(tKm / 800 * 60);
  var tTime = tMins >= 120 ? (tMins/60).toFixed(1) + 'h' : tMins + ' min';
  var s = 'Bergen to Troms\\u00f8 is ' + tKm.toLocaleString() + ' km \\u2014 about the same as Bergen to Paris (' + pKm.toLocaleString() + ' km). ';
  if (Math.abs(km - tKm) < 150) {
    s += 'For comparison, ' + name + ' is almost exactly the same distance (' + km.toLocaleString() + ' km) \\u2014 you\\u2019d travel as far to reach ' + name + ' as to reach Arctic Norway.';
  } else if (km < tKm) {
    s += 'For comparison, ' + name + ' is only ' + km.toLocaleString() + ' km away \\u2014 a shorter trip than to Norway\\u2019s own Arctic north.';
  } else if (km < tKm * 2) {
    s += 'For comparison, ' + name + ' is ' + km.toLocaleString() + ' km away \\u2014 not that much further than Troms\\u00f8.';
  } else {
    s += 'For comparison, even ' + name + ', at ' + km.toLocaleString() + ' km, is only ' + (km / tKm).toFixed(1) + '\\u00d7 the Bergen\\u2013Troms\\u00f8 distance.';
  }
  var pMins = Math.round(pToC / 800 * 60);
  var pTime = pMins >= 120 ? Math.floor(pMins/60) + 'h and ' + (pMins%60) + ' min' : pMins + ' min';
  var bpMins = Math.round(pKm / 800 * 60);
  var ratio = pKm / pToC;
  function ratioTextEn(r) {
    if (r >= 1.8 && r <= 2.2) return 'twice as fast';
    if (r >= 2.8 && r <= 3.2) return 'three times faster';
    if (r >= 3.8 && r <= 4.2) return 'four times faster';
    return 'about ' + r.toFixed(1) + '\\u00d7 faster';
  }
  if (ratio > 1.3) {
    s += ' On the other hand, Paris\\u2013' + name + ' takes ' + pTime + ' by plane, ' + ratioTextEn(ratio) + ' than Paris\\u2013Bergen.';
  } else if (pToC > pKm * 1.15) {
    s += ' Interestingly, Paris\\u2013' + name + ' (' + pToC.toLocaleString() + ' km) is even longer than Paris\\u2013Bergen.';
  } else {
    s += ' Paris\\u2013' + name + ' is about the same distance as Paris\\u2013Bergen (' + pToC.toLocaleString() + ' km).';
  }
  return s;
}`;

const distTextFr = `function(name, km, tKm, pKm, pToC) {
  var s = 'Bergen\\u2013Troms\\u00f8 fait ' + tKm.toLocaleString('fr') + ' km \\u2014 \\u00e0 peu pr\\u00e8s autant que Bergen\\u2013Paris (' + pKm.toLocaleString('fr') + ' km). ';
  if (Math.abs(km - tKm) < 150) {
    s += 'En comparaison, ' + name + ' est presque \\u00e0 la m\\u00eame distance (' + km.toLocaleString('fr') + ' km) \\u2014 il faut voyager aussi loin pour atteindre ' + name + ' que pour rejoindre la Norv\\u00e8ge arctique.';
  } else if (km < tKm) {
    s += 'En comparaison, ' + name + " n'est qu'\\u00e0 " + km.toLocaleString('fr') + ' km \\u2014 un trajet plus court que vers le nord arctique de la Norv\\u00e8ge.';
  } else if (km < tKm * 2) {
    s += 'En comparaison, ' + name + ' est \\u00e0 ' + km.toLocaleString('fr') + ' km \\u2014 pas beaucoup plus loin que Troms\\u00f8.';
  } else {
    s += 'En comparaison, m\\u00eame ' + name + ', \\u00e0 ' + km.toLocaleString('fr') + ' km, ne repr\\u00e9sente que ' + (km / tKm).toFixed(1) + '\\u00d7 la distance Bergen\\u2013Troms\\u00f8.';
  }
  var pMins = Math.round(pToC / 800 * 60);
  var pTime = pMins >= 120 ? Math.floor(pMins/60) + 'h et ' + (pMins%60) + ' min' : pMins + ' min';
  var bpMins = Math.round(pKm / 800 * 60);
  var ratio = pKm / pToC;
  function ratioTextFr(r) {
    if (r >= 1.8 && r <= 2.2) return 'deux fois plus rapide';
    if (r >= 2.8 && r <= 3.2) return 'trois fois plus rapide';
    if (r >= 3.8 && r <= 4.2) return 'quatre fois plus rapide';
    return 'environ ' + r.toFixed(1) + '\\u00d7 plus rapide';
  }
  if (ratio > 1.3) {
    s += " D'autre part, Paris\\u2013" + name + ' ne prend que ' + pTime + ' en avion, ' + ratioTextFr(ratio) + ' que Paris\\u2013Bergen.';
  } else if (pToC > pKm * 1.15) {
    s += ' Fait int\\u00e9ressant, Paris\\u2013' + name + ' (' + pToC.toLocaleString('fr') + ' km) est m\\u00eame plus long que Paris\\u2013Bergen.';
  } else {
    s += ' Paris\\u2013' + name + ' est \\u00e0 peu pr\\u00e8s la m\\u00eame distance que Paris\\u2013Bergen (' + pToC.toLocaleString('fr') + ' km).';
  }
  return s;
}`;

function buildI18nJson(lang) {
  const strings = i18nData[lang];
  // Build a JS object literal string (not pure JSON — includes a function)
  const entries = Object.entries(strings).map(([k, v]) => {
    return `  ${JSON.stringify(k)}: ${JSON.stringify(v)}`;
  });
  const distText = lang === 'fr' ? distTextFr : distTextEn;
  entries.push(`  "dist_text": ${distText}`);
  return '{\n' + entries.join(',\n') + '\n}';
}

function buildLangToggle(lang, isAbout) {
  const enActive = lang === 'en' ? ' class="active"' : '';
  const frActive = lang === 'fr' ? ' class="active"' : '';

  let enHref, frHref, aboutHref;
  if (isAbout) {
    enHref = `${base}/en/about.html`;
    frHref = `${base}/fr/about.html`;
    aboutHref = null; // already on about
  } else {
    enHref = `${base}/en/`;
    frHref = `${base}/fr/`;
    aboutHref = lang === 'fr' ? `${base}/fr/about.html` : `${base}/en/about.html`;
  }

  let html = '';
  html += `<a href="${enHref}" style="padding:4px 12px;border-radius:14px;transition:all 0.25s ease;user-select:none;text-decoration:none;color:var(--text)"${enActive}>EN</a>`;
  html += `<a href="${frHref}" style="padding:4px 12px;border-radius:14px;transition:all 0.25s ease;user-select:none;text-decoration:none;color:var(--text)"${frActive}>FR</a>`;
  if (aboutHref) {
    const aboutLabel = lang === 'fr' ? '\u00c0 propos' : 'About';
    html += `<a href="${aboutHref}" class="about-link">${aboutLabel}</a>`;
  }
  return html;
}

function extractTextContent(node) {
  if (!node) return '';
  if (typeof node === 'string') return node;
  // Markdoc text nodes store content in attributes.content
  if (node.type === 'text' && node.attributes && node.attributes.content) {
    return node.attributes.content;
  }
  if (node.children) {
    return node.children.map(extractTextContent).join('');
  }
  return '';
}

function buildToc(ast) {
  const links = [];
  const idPattern = /\s*\{#([^}]+)\}\s*$/;

  function walk(node) {
    if (!node) return;
    if (node.type === 'heading') {
      const level = node.attributes && node.attributes.level;
      if (level === 2 || level === 3) {
        let rawText = extractTextContent(node);
        // Extract {#id} annotation from text
        let id = node.attributes && node.attributes.id;
        const idMatch = rawText.match(idPattern);
        if (idMatch) {
          id = idMatch[1];
          rawText = rawText.replace(idPattern, '').trim();
        }
        if (!id) {
          id = rawText.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        }
        const isSub = level === 3;
        links.push(`<a href="#${id}"${isSub ? ' class="sub"' : ''}>${rawText}</a>`);
      }
    }
    if (node.children) {
      for (const child of node.children) {
        walk(child);
      }
    }
  }

  walk(ast);
  return links.join('\n    ');
}

const labels = {
  en: {
    footer: 'A project by <a href="https://linkedin.com/in/cedriclombion" style="color:var(--muted)">C\u00e9dric Lombion</a>. Data: <a href="https://open-meteo.com/" style="color:var(--muted)">Open-Meteo</a> (CC BY 4.0). Code: MIT. <a href="https://github.com/clombion/bergen-paris-weather" style="color:var(--muted)">GitHub</a>.',
    backTop: 'Back to top',
    snowLabel: 'Snow days only',
    searchPlaceholder: 'Filter by date, e.g. 2022-01',
  },
  fr: {
    footer: 'Un projet de <a href="https://linkedin.com/in/cedriclombion" style="color:var(--muted)">C\u00e9dric Lombion</a>. Donn\u00e9es\u00a0: <a href="https://open-meteo.com/" style="color:var(--muted)">Open-Meteo</a> (CC BY 4.0). Code\u00a0: MIT. <a href="https://github.com/clombion/bergen-paris-weather" style="color:var(--muted)">GitHub</a>.',
    backTop: 'Retour en haut',
    snowLabel: 'Jours de neige uniquement',
    searchPlaceholder: 'Filtrer par date, ex. 2022-01',
  },
};

// Compute data base path (relative from output to dist/site/data/)
function getDataBase(outputPath) {
  const outputDir = path.dirname(outputPath);
  const dataDir = path.join('dist', 'site', 'data');
  let rel = path.relative(outputDir, dataDir);
  rel = rel.replace(/\\/g, '/');
  if (!rel.endsWith('/')) rel += '/';
  return rel;
}

// Compute styles base path (relative from output to dist/styles/)
function getStylesBase(outputPath) {
  const outputDir = path.dirname(outputPath);
  const stylesDir = path.join('dist', 'styles');
  let rel = path.relative(outputDir, stylesDir);
  rel = rel.replace(/\\/g, '/');
  if (!rel.endsWith('/')) rel += '/';
  return rel;
}

// Ensure directory exists
function mkdirp(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

// Copy directory recursively
function copyDirSync(src, dest) {
  mkdirp(dest);
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Main build
let built = 0;
let skipped = 0;

for (const page of pages) {
  const contentPath = path.resolve(page.content);
  const templatePath = path.resolve(page.template);
  const outputPath = path.resolve(page.output);

  // Check content file exists
  if (!fs.existsSync(contentPath)) {
    console.log(`  skip: ${page.content} (not found)`);
    skipped++;
    continue;
  }

  // Read and parse Markdoc content
  const source = fs.readFileSync(contentPath, 'utf-8');
  const ast = Markdoc.parse(source);

  // Extract frontmatter
  let frontmatter = {};
  if (ast.attributes && ast.attributes.frontmatter) {
    try {
      frontmatter = yaml.load(ast.attributes.frontmatter) || {};
    } catch (e) {
      console.warn(`  warn: failed to parse frontmatter in ${page.content}:`, e.message);
    }
  }

  // Transform
  const config = {
    tags,
    variables: { lang: page.lang },
  };
  const transformed = Markdoc.transform(ast, config);
  const contentHtml = Markdoc.renderers.html(transformed);

  // Read template
  const template = fs.readFileSync(templatePath, 'utf-8');

  // Determine page type
  const isAbout = page.template.includes('about');
  const isIndex = !isAbout;

  // Build replacements
  const title = frontmatter.title || (isAbout
    ? (page.lang === 'fr' ? '\u00c0 propos \u2014 Bergen vs Paris' : 'About \u2014 Bergen vs Paris')
    : (page.lang === 'fr' ? 'Bergen vs Paris \u2014 La surprise hivernale' : 'Bergen vs Paris \u2014 The Winter Surprise'));

  const langToggle = buildLangToggle(page.lang, isAbout);
  const toc = isAbout ? buildToc(ast) : '';
  const dataBase = getDataBase(page.output);
  const stylesBase = getStylesBase(page.output);
  const i18nJson = isIndex ? buildI18nJson(page.lang) : '{}';
  const footer = labels[page.lang].footer;
  const backTopText = labels[page.lang].backTop;
  const snowLabel = labels[page.lang].snowLabel;
  const searchPlaceholder = labels[page.lang].searchPlaceholder;

  // Replace placeholders
  let html = template;
  html = html.replace(/\{\{CONTENT\}\}/g, contentHtml);
  html = html.replace(/\{\{LANG\}\}/g, page.lang);
  html = html.replace(/\{\{TITLE\}\}/g, title);
  html = html.replace(/\{\{LANG_TOGGLE\}\}/g, langToggle);
  html = html.replace(/\{\{TOC\}\}/g, toc);
  html = html.replace(/\{\{DATA_BASE\}\}/g, dataBase);
  html = html.replace(/\{\{STYLES_BASE\}\}/g, stylesBase);
  html = html.replace(/\{\{I18N_JSON\}\}/g, i18nJson);
  html = html.replace(/\{\{FOOTER\}\}/g, footer);
  html = html.replace(/\{\{BACK_TOP_TEXT\}\}/g, backTopText);
  html = html.replace(/\{\{SNOW_LABEL\}\}/g, snowLabel);
  html = html.replace(/\{\{SEARCH_PLACEHOLDER\}\}/g, searchPlaceholder);

  // Write output
  mkdirp(path.dirname(outputPath));
  fs.writeFileSync(outputPath, html, 'utf-8');
  console.log(`  built: ${page.output}`);
  built++;
}

// Write root redirect to /en/
const redirectHtml = `<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=${base}/en/"><link rel="canonical" href="${base}/en/"></head></html>`;
fs.writeFileSync(path.resolve('dist', 'index.html'), redirectHtml);
console.log('  built: dist/index.html (redirect → /en/)');

// Copy data files
const dataSrc = path.resolve('site', 'data');
const dataDest = path.resolve('dist', 'site', 'data');
if (fs.existsSync(dataSrc)) {
  copyDirSync(dataSrc, dataDest);
  console.log(`  copied: site/data/ -> dist/site/data/`);
} else {
  console.warn('  warn: site/data/ not found, skipping data copy');
}

// Copy styles
const stylesSrc = path.resolve('styles');
const stylesDest = path.resolve('dist', 'styles');
if (fs.existsSync(stylesSrc)) {
  copyDirSync(stylesSrc, stylesDest);
  console.log(`  copied: styles/ -> dist/styles/`);
} else {
  console.warn('  warn: styles/ not found, skipping styles copy');
}

console.log(`\nDone: ${built} pages built, ${skipped} skipped.`);
