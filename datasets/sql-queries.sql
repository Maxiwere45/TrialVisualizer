use trial_visualizer

// Publications du mois courant (ex mai 2020) triées par score altmetric décroissant et départagées par citations décroissantes
// FONCTIONNEL
db.Publications.aggregate([
  {
    $match: {
      datePublished: {
        $gte: "2020-05-01",
        $lt: "2020-06-01"
      }
    }
  },
  {
    $sort: {
      altmetric: -1,
      timesCited: -1
    }
  }
])

// Nombre d'essais en phase 1 / 2 / 3 / 4 ["CHICTR2000032400" a retirer]
// FONCTIONNEL
db.ClinicalTrials.aggregate([
  {
    $group: {
      _id: "$phase",
      count: { $sum: 1 }
    }
  }
])

// Nombre d'essais par genre [ Attention, il y a des valeurs null ]
// FONCTIONNEL
db.ClinicalTrials.aggregate([
  {
    $group: {
      _id: "$gender",
      count: { $sum: 1 }
    }
  }
])

db.ClinicalTrials.findOne(
  { id: "ISRCTN10077335" },
  { interventions: 1, _id: 0 }
)

// Nombre d'essais par type d'intervention
// FONCTIONNEL
db.ClinicalTrials.aggregate([
  {
    $unwind: "$interventions"
  },
  {
    $group: {
      _id: "$interventions.arm_group_labels",
      count: { $sum: 1 }
    }
  }
])

// arm_group_labels: [ 'Drug' ]
// FONCTIONNEL
db.ClinicalTrials.find({
   "interventions.arm_group_labels": /Drug/i
});