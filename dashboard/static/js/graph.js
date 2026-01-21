var network = null;
var nodes = new vis.DataSet([]);
var edges = new vis.DataSet([]);

function initNetwork() {
    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        nodes: {
            shape: 'dot',
            size: 16,
            font: {
                color: '#00ff00',
                face: 'Roboto Mono'
            },
            borderWidth: 1,
            color: {
                background: '#000',
                border: '#00ff00',
                highlight: {
                    background: '#0a0a0a',
                    border: '#fff'
                }
            }
        },
        edges: {
            width: 1,
            color: { color: '#003300', highlight: '#00ff00' },
            smooth: {
                type: 'continuous'
            }
        },
        physics: {
            stabilization: false,
            barnesHut: {
                gravitationalConstant: -8000,
                springConstant: 0.04,
                springLength: 95
            },
        },
        interaction: {
            tooltipDelay: 200,
            hideEdgesOnDrag: true
        }
    };
    network = new vis.Network(container, data, options);
}

function processData(rawData) {
    nodes.clear();
    edges.clear();

    // Central Node (Implicit - we might need to define a target later, reusing 'Target' for now)
    var centerId = 'TARGET';
    nodes.add({ id: centerId, label: 'TARGET', size: 30, color: { background: '#ff0000', border: '#ff0000' } });

    // Categories colors
    const colors = {
        social: '#00ff00',
        email: '#00ccff',
        phone: '#ffcc00',
        crypto: '#ff6600',
        domain: '#cc00ff',
        image: '#ffffff'
    };

    // Process Usernames
    for (const [user, platforms] of Object.entries(rawData.usernames)) {
        nodes.add({ id: user, label: user, group: 'social', color: { border: colors.social, background: '#000' } });
        edges.add({ from: centerId, to: user });

        for (const [site, url] of Object.entries(platforms)) {
            // Avoid duplicates if multiple usernames find same site url (rare but possible)
            if (!nodes.get(url)) {
                nodes.add({
                    id: url,
                    label: site,
                    group: 'site',
                    shape: 'diamond',
                    title: url, // Tooltip
                    color: { border: '#aaa', background: '#000' }
                });
            }
            edges.add({ from: user, to: url });
        }
    }

    // Process Emails
    for (const [email, details] of Object.entries(rawData.emails)) {
        nodes.add({ id: email, label: email, group: 'email', color: { border: colors.email, background: '#000' } });
        edges.add({ from: centerId, to: email });

        if (details.gravatar) {
            nodes.add({ id: details.gravatar, label: 'Gravatar', shape: 'image', image: details.gravatar });
            edges.add({ from: email, to: details.gravatar });
        }
    }

    // Process Phones
    for (const [phone, details] of Object.entries(rawData.phones)) {
        nodes.add({ id: phone, label: phone, group: 'phone', color: { border: colors.phone, background: '#000' } });
        edges.add({ from: centerId, to: phone });
    }

    // Crypto
    rawData.crypto.forEach(wallet => {
        nodes.add({ id: wallet, label: wallet.substring(0, 8) + '...', group: 'crypto', color: { border: colors.crypto, background: '#000' } });
        edges.add({ from: centerId, to: wallet });
    });

    // Domains
    rawData.domains.forEach(domain => {
        nodes.add({ id: domain, label: domain, group: 'domain', color: { border: colors.domain, background: '#000' } });
        edges.add({ from: centerId, to: domain });
    });

    // Images
    rawData.images.forEach(img => {
        nodes.add({ id: img, label: 'Image', group: 'image', shape: 'square', color: { border: colors.image, background: '#000' } });
        edges.add({ from: centerId, to: img });
    });

    document.getElementById('status').innerText = `Nodes: ${nodes.length} | Edges: ${edges.length}`;
}

function refreshData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                document.getElementById('status').innerText = "No Data Found";
            } else {
                processData(data);
            }
        })
        .catch(err => console.error(err));
}

function togglePhysics() {
    network.physics.options.enabled = !network.physics.options.enabled;
    network.setOptions({ physics: { enabled: network.physics.options.enabled } });
}

// Start
initNetwork();
refreshData();
setInterval(refreshData, 5000); // Auto-refresh every 5s
