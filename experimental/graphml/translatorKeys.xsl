<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:gra = "http://graphml.graphdrawing.org/xmlns">
    
    <xsl:template match="/">
        {
        <xsl:for-each select="gra:graphml/gra:key"> 
            "<xsl:value-of select="@for"/>_<xsl:value-of select="@id"/>" : "<xsl:value-of select="@attr.name"/>"<xsl:if test="position() != last()">,</xsl:if></xsl:for-each>
        <xsl:for-each select="gra:graphml/gra:graph">, "title" : "<xsl:value-of select="@id"/>"</xsl:for-each>
                      
            
       
        }

      
      
  </xsl:template>
    
   
</xsl:stylesheet>