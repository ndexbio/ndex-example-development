<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:gra = "http://graphml.graphdrawing.org/xmlns">
    
    <xsl:template match="/">
[
    {
       "nodes":
        [
           <xsl:for-each select="gra:graphml/gra:graph/gra:node">
               {
                   "@id":<xsl:value-of select="@id"/>,<xsl:for-each select="gra:data">
                    "node_<xsl:value-of select= "@key"/>": "<xsl:value-of select= "."/>"<xsl:if test="position() != last()">, </xsl:if>
               </xsl:for-each>
               }<xsl:if test="position() != last()">, </xsl:if>
               
           </xsl:for-each>
        
        ]
    },
    {
        "edges": 
        [
        
            <xsl:for-each select="gra:graphml/gra:graph/gra:edge">
               {
                    "s": <xsl:value-of select="@source"/>,
                    "t": <xsl:value-of select="@target"/>,<xsl:for-each select="gra:data">
                    "edge_<xsl:value-of select= "@key"/>": "<xsl:value-of select= "."/>"<xsl:if test="position() != last()">, </xsl:if>
               </xsl:for-each>
            }<xsl:if test="position() != last()">, </xsl:if>
         </xsl:for-each>
        
        ]
    },
    {
        "networkAttributes": 
        [
        
        <xsl:for-each select="gra:graphml/gra:graph">
               {
                    <xsl:for-each select="gra:data">
                    "graph_<xsl:value-of select= "@key"/>": "<xsl:value-of select= "."/>"<xsl:if test="position() != last()">, </xsl:if>
               </xsl:for-each>
            }<xsl:if test="position() != last()">, </xsl:if>
         </xsl:for-each>
        
        ]
    },
    
    {
        "nodeAttributes": 
        [
        ]
    },

    {
        "edgeAttributes": 
        [
        ]
    }
        
]

      
      
  </xsl:template>
    
   
</xsl:stylesheet>