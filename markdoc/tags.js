const { Tag } = require('@markdoc/markdoc');

const chart = {
  render: 'div',
  selfClosing: true,
  attributes: {
    id: { type: String, required: true },
    height: { type: Number, default: 300 },
    'fixed-height': { type: Boolean, default: false },
  },
  transform(node, config) {
    const attrs = node.transformAttributes(config);
    const id = attrs.id;
    const height = attrs.height;
    const fixedHeight = attrs['fixed-height'];

    const wrapperAttrs = { class: 'chart-wrap' };
    const canvasAttrs = { id };

    if (fixedHeight) {
      wrapperAttrs.style = `position:relative;height:${height}px`;
    } else {
      canvasAttrs.height = String(height);
    }

    return new Tag('div', wrapperAttrs, [new Tag('canvas', canvasAttrs, [])]);
  },
};

const stats = {
  render: 'div',
  selfClosing: true,
  attributes: {
    id: { type: String, required: true },
    classes: { type: String, default: '' },
  },
  transform(node, config) {
    const attrs = node.transformAttributes(config);
    const className = ['stat-grid', attrs.classes].filter(Boolean).join(' ');
    return new Tag('div', { id: attrs.id, class: className }, []);
  },
};

const callout = {
  render: 'div',
  attributes: {},
  transform(node, config) {
    const children = node.transformChildren(config);
    return new Tag('div', { class: 'highlight-box' }, children);
  },
};

const heatmap = {
  render: 'div',
  selfClosing: true,
  attributes: {},
  transform(node, config) {
    const lang = (config.variables && config.variables.lang) || 'en';
    const labels =
      lang === 'fr'
        ? { all: 'Tout', close: 'Proches', typical: 'Moyens', far: '\u00c9loign\u00e9s' }
        : { all: 'All', close: 'Similar', typical: 'Average', far: 'Different' };

    return new Tag('div', {}, [
      new Tag(
        'div',
        { class: 'segmented', id: 'heatmapFilter' },
        [
          new Tag('div', { class: 'seg-slider' }, []),
          new Tag(
            'button',
            { class: 'seg-btn active', 'data-filter': 'all' },
            [labels.all]
          ),
          new Tag(
            'button',
            { class: 'seg-btn', 'data-filter': 'close' },
            [labels.close]
          ),
          new Tag(
            'button',
            { class: 'seg-btn', 'data-filter': 'typical' },
            [labels.typical]
          ),
          new Tag(
            'button',
            { class: 'seg-btn', 'data-filter': 'far' },
            [labels.far]
          ),
        ]
      ),
      new Tag(
        'div',
        { class: 'chart-wrap', style: 'overflow-x:auto' },
        [
          new Tag(
            'div',
            { id: 'heatmap', class: 'heatmap-grid', style: 'min-width:500px' },
            []
          ),
        ]
      ),
    ]);
  },
};

const yearSlider = {
  render: 'div',
  selfClosing: true,
  attributes: {},
  transform(node, config) {
    return new Tag(
      'div',
      {
        class: 'year-slider-wrapper',
      },
      [
        new Tag('span', {}, ['2016']),
        new Tag('input', {
          type: 'range',
          id: 'yearSlider',
          min: '2016',
          max: '2025',
          value: '2025',
          step: '1',
          style: 'flex:1;accent-color:#b0ada4;cursor:pointer',
        }),
        new Tag('span', {}, ['2025']),
        new Tag(
          'span',
          {
            id: 'yearLabel',
            style:
              'font-weight:600;color:var(--text);min-width:3em;text-align:center',
          },
          ['2025']
        ),
      ]
    );
  },
};

const flightMap = {
  render: 'div',
  selfClosing: true,
  attributes: {},
  transform(node, config) {
    return new Tag('div', { style: 'margin:16px 0' }, [
      new Tag('canvas', { id: 'flightMap', height: '480' }, []),
    ]);
  },
};

const capitalSelect = {
  render: 'select',
  selfClosing: true,
  attributes: {},
  transform(node, config) {
    return new Tag(
      'select',
      { id: 'capitalSelect', class: 'capital-select' },
      []
    );
  },
};

const dataTable = {
  render: 'div',
  selfClosing: true,
  attributes: {},
  transform(node, config) {
    const lang = (config.variables && config.variables.lang) || 'en';
    const snowLabel =
      lang === 'fr' ? 'Jours de neige uniquement' : 'Snow days only';
    const searchPlaceholder =
      lang === 'fr'
        ? 'Filtrer par date, ex. 2022-01'
        : 'Filter by date, e.g. 2022-01';

    return new Tag('div', { class: 'data-explorer' }, [
      new Tag(
        'div',
        {
          class: 'data-controls',
        },
        [
          new Tag('input', {
            type: 'text',
            id: 'dataSearch',
            placeholder: searchPlaceholder,
            style:
              'padding:6px 12px;border:1px solid var(--border);border-radius:6px;font-family:inherit;font-size:inherit;width:200px',
          }),
          new Tag(
            'label',
            {
              style:
                'color:var(--muted);display:flex;align-items:center;gap:4px',
            },
            [
              new Tag('input', { type: 'checkbox', id: 'snowOnly' }),
              new Tag('span', { id: 'snowLabel' }, [snowLabel]),
            ]
          ),
          new Tag('span', { id: 'rowCount', style: 'color:var(--muted)' }, []),
        ]
      ),
      new Tag(
        'div',
        {
          class: 'data-scroll',
        },
        [
          new Tag(
            'table',
            { id: 'dataTable', style: 'margin:0;width:100%' },
            [
              new Tag(
                'thead',
                {
                  id: 'dataHead',
                  style: 'position:sticky;top:0;background:var(--card)',
                },
                []
              ),
              new Tag('tbody', { id: 'dataBody' }, []),
            ]
          ),
        ]
      ),
    ]);
  },
};

const byline = {
  render: 'div',
  selfClosing: false,
  transform(node, config) {
    const children = node.transformChildren(config);
    return new Tag('div', {
      class: 'byline',
    }, children);
  },
};

const legend = {
  render: 'div',
  selfClosing: true,
  attributes: {},
  transform(node, config) {
    return new Tag('div', { class: 'legend-inline' }, [
      new Tag('span', {}, [
        new Tag('span', { class: 'legend-dot', style: 'background:var(--bergen)' }, []),
        ' Bergen',
      ]),
      new Tag('span', {}, [
        new Tag('span', { class: 'legend-dot', style: 'background:var(--paris)' }, []),
        ' Paris',
      ]),
    ]);
  },
};

const section = {
  render: 'section',
  attributes: {
    id: { type: String },
  },
  transform(node, config) {
    const attrs = node.transformAttributes(config);
    const children = node.transformChildren(config);
    const sectionAttrs = {};
    if (attrs.id) sectionAttrs.id = attrs.id;
    return new Tag('section', sectionAttrs, children);
  },
};

const methodology = {
  render: 'div',
  transform(node, config) {
    const children = node.transformChildren(config);
    return new Tag('div', { class: 'methodology' }, children);
  },
};

const headerTag = {
  render: 'header',
  transform(node, config) {
    const children = node.transformChildren(config);
    return new Tag('header', {}, children);
  },
};

const distanceSummary = {
  render: 'p',
  selfClosing: true,
  transform(node, config) {
    return new Tag('p', { id: 'distanceSummary', class: 'lead', style: 'margin-top:8px' }, []);
  },
};

const stepMeta = {
  render: 'div',
  selfClosing: true,
  attributes: {
    items: { type: String, required: true },
  },
  transform(node, config) {
    const attrs = node.transformAttributes(config);
    const items = attrs.items.split(',').map(s => s.trim()).filter(Boolean);
    return new Tag('div', { class: 'step-meta' },
      items.map(item => new Tag('span', {}, [item]))
    );
  },
};

const heading = {
  children: ['inline'],
  attributes: {
    id: { type: String },
    level: { type: Number, required: true, default: 1 },
  },
  transform(node, config) {
    const children = node.transformChildren(config);
    // Extract text content for auto-ID
    function getText(c) {
      if (typeof c === 'string') return c;
      if (c && c.children) return c.children.map(getText).join('');
      return '';
    }
    const text = children.map(getText).join('');
    const id = node.attributes.id || text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
    return new Tag(`h${node.attributes.level}`, { id }, children);
  },
};

module.exports = {
  tags: {
    chart,
    stats,
    callout,
    heatmap,
    'year-slider': yearSlider,
    'flight-map': flightMap,
    'capital-select': capitalSelect,
    'data-table': dataTable,
    byline,
    legend,
    section,
    methodology,
    'distance-summary': distanceSummary,
    header: headerTag,
    'step-meta': stepMeta,
  },
  nodes: {
    heading,
  },
};
