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

// Groupement des essais selon les interventions (colonne intervention),
    -- en particulier ceux avec un arm_group_label = Drug

db.ClinicalTrials.aggregate([
  {
    $unwind: "$interventions"
  },
  {
    $match: {
      "interventions.type": "Drug"
    }
  },
  {
    $group: {
      _id: "$interventions.name",
      count: { $sum: 1 }
    }
  },
  {
    $sort: {
      count: -1
    }
  }
]);


// Recherche d'Ivermectin dans les essais
db.ClinicalTrials.find({ "interventions.name": { $regex: /ivermectin/i } })

// Recherche d'Ivermectin dans les publications
db.Publications.find({ $or: [
  { "title": { $regex: /ivermectin/i } },
  { "abstract": { $regex: /ivermectin/i } },
  { "concepts": { $regex: /ivermectin/i } },
  { "meshTerms": { $regex: /ivermectin/i } }
] })

// Publications du mois courant (ex mai 2020) avec
// triées par score altmetric décroissant et
// départagées par citations décroissantes
db.Publications.aggregate([{
    $match: {
        datePublished: {
        $gte: '2020-05-01',
        $lt: '2020-06-01'
        },
        doctype: {
            $ne: 'preprint'
        }
    }},
    {
        $sort: {
            altmetric: -1,
            timesCited: -1
        }
    }]);

// Détermination des concepts les plus fréquents dans les publications (hors preprints pour une période donnée) :
db.Publications.aggregate([
    { $unwind: "$concepts" },
    { $group: { _id: "$concepts", count: { $sum: 1 } } },
    { $match: { "openAccess": { $not: /green_sub/ } } },
    //{ $match: { "year" : 2020}},
    { $sort: { count: -1 } },
    //{ $limit: 20 }
]);
