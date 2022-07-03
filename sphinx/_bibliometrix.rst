Bibliometrix
#########################################################################################

.. raw:: html

   <hr style="height:4px;border-width:0;color:gray;background-color:black">


In this section, the library's functionalities are presented in the structure used 
internally in Bibliometrix, in order to facilitate comparison. Likewise, functions have
been created with the same names as the Bibliometrix menus to facilitate the use of the
tool by users. It should be noted that the functions presented in this section cover only
a part of TechMiner's capabilities, and in this sense, Bibliometrix contains only a 
subset of the analytical capabilities of TechMiner.


.. toctree::
   :maxdepth: 1
   
   bibliometrix/overview/_index


Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   See ``Import Scopus Files`` in `Data <_user_data.html>`__. 


Filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::

      user_filters


Overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
   .. toctree::

      main_information
      annual_scientific_production
      average_citations_per_year

   TODO:

   .. toctree::

      three_fields_plot


Sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      most_frequent_sources

   .. toctree::
      most_local_cited_sources

   .. toctree::
      sources_production_over_time
   
   .. toctree::
      bradford_law     
      core_sources

   .. toctree::
      source_impact

   .. toctree::
      source_dynamics_table
      source_dynamics_plot

   .. toctree::
      most_global_cited_sources_in_refs


Authors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      most_frequent_authors

   .. toctree::      
      most_local_cited_authors

   .. toctree::      
      authors_production_over_time
      authors_production_per_year
      documents_by_author

   .. toctree::
      author_impact
      
   .. toctree::
      most_global_cited_authors_in_refs



   TODO:

   .. toctree::
      lotka_law    
      


Institutions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      most_frequent_institutions

   .. toctree::      
      most_local_cited_institutions

   .. toctree::      
      institutions_production_over_time

   .. toctree::
      institution_impact

   .. toctree::      
      institutions_production_per_year

   **New:**

   .. toctree::
      most_global_cited_institutions_in_refs
      


Countries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      most_frequent_countries

   .. toctree::      
      most_local_cited_countries

   .. toctree::      
      countries_production_over_time

   .. toctree::
      country_impact

   .. toctree::
      countries_production_per_year

   .. toctree::      
      country_scientific_production


   **New:**

   .. toctree::
      most_global_cited_countries_in_refs


   TODO:

   .. toctree::
      :maxdepth: 1
      
      corresponding_authors_country


Documents 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      most_global_cited_documents

   .. toctree::
      most_local_cited_documents

   .. toctree::      
      documents_by_country
      documents_by_institution

   **New:**

   .. toctree::
      num_documents_by_type
      global_citations_by_type
      local_citations_by_type


Cited References
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      most_local_cited_references


   **New:**

   .. toctree::
      most_global_cited_references


   TODO:

   .. toctree::
      :maxdepth: 1

      rpys


Citing Documents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   **New:**

   .. toctree::




Words
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      :maxdepth: 1

      most_frequent_words
      word_cloud
      tree_map
      word_dynamics_plot
      word_dynamics_table

   **New:**

   .. toctree::


   TODO:

   .. toctree::
      :maxdepth: 1
      
      topic_dynamics
      trend_topics



Clustering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      :maxdepth: 1


   **New:**

   .. toctree::


   .. toctree::
      :maxdepth: 1

      coupling_matrix
      coupling_network_communities
      coupling_network_degree_plot
      coupling_network_graph


Conceptual Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. raw:: html

      <p style="color:gray">Network Approach:</p>


   .. toctree::
      :maxdepth: 1

      co_occurrence_network_communities
      co_occurrence_network_degree_plot
      co_occurrence_network_graph
      co_occurrence_network_indicators
      co_occurrence_network_summarization



   .. toctree::
      :maxdepth: 1

      thematic_map_communities
      thematic_map_degree_plot
      thematic_map_indicators
      thematic_map_network
      thematic_map_strategic_diagram
      thematic_map_summarization

   .. toctree::
      :maxdepth: 1

      thematic_evolution_plot

   .. raw:: html

      <p style="color:gray">Factorial Approach:</p>

   .. toctree::
      :maxdepth: 1

      factorial_analysis_mds_communities
      factorial_analysis_mds_data
      factorial_analysis_mds_map
      factorial_analysis_mds_silhouette_scores

   * ``TODO: Factorial Approach / CA``

   **New:**

   .. toctree::



Intellectual Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. toctree::
      :maxdepth: 1

      co_citation_network_communities
      co_citation_network_degree_plot
      co_citation_network_graph    
      co_citation_network_indicators


   **New:**

   .. toctree::


   .. Note::
      In addition, **TechMiner** implements the following functions:

         .. toctree::
               :maxdepth: 1

               co_citation_matrix    
               main_path_network


   * ``TODO: Historiograph``






Social Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. note:: 
      A collaboration network is a generic co-occurrence network where the analized column
      is restricted to the following columns in the dataset:

      * Authors.

      * Institutions. 

      * Countries.

      As a consequence, many implemented plots and analysis are valid for analyzing a 
      co-occurrence network, including heat maps and other plot types.

   .. toctree::
      :maxdepth: 1

      collaboration_network_communities
      collaboration_network_degree_plot
      collaboration_network_graph
      collaboration_network_indicators
      

   **New:**

   .. toctree::


   * ``TODO: Collaboration WorldMap``