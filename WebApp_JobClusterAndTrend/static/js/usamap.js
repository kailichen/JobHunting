var map = new Datamap({
  scope: 'usa',
  element: document.getElementById('usamap'),
  geographyConfig: {
    highlightBorderColor: '#bada55',
   popupTemplate: function(geography, data) {
      return '<div class="hoverinfo">' + geography.properties.name + ' Job Hunts:' +  data.JobHunts + ' '
    },
    highlightBorderWidth: 3
  },

  fills: {
  'Probability': '#306596',
  defaultFill: '#306596'
},
data:{
  "AZ": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "CO": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "DE": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "FL": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "GA": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "HI": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "ID": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "IL": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "IN": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "IA": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "KS": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "KY": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "LA": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "MD": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "ME": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "MA": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "MN": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "MI": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "MS": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "MO": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "MT": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "NC": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "NE": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "NV": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "NH": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "NJ": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "NY": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "ND": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "NM": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "OH": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "OK": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "OR": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "PA": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "RI": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "SC": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "SD": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "TN": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "TX": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "UT": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "WI": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "VA": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "VT": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "WA": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "WV": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "WY": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "CA": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "CT": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "AK": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "AR": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  },
  "AL": {
      "fillKey": "Probability",
      "JobHunts": "N/A"
  }
}
});
map.labels();