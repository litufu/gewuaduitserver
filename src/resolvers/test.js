

const res = [ { holder_name: '李土福', ratio: '99.00%' },
{ holder_name: '李永红', ratio: '1.00%' } ]

for (let i=0;i<res.length;i++) {
    const ratio = parseFloat(res[i].ratio.replace('%'))
    const name = res[i].holder_name
    console.log(ratio)
    console.log(name)
}


