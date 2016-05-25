<xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:mods="http://www.loc.gov/mods/v3">
	<xsl:output method="xml" indent="yes"/>

	<xsl:template match="recordlist">
		<mods:modsCollection xmlns:xlink="http://www.w3.org/1999/xlink"
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
			xmlns="http://www.loc.gov/mods/v3"
			xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-3.xsd">
			<xsl:apply-templates select="record"/>
		</mods:modsCollection>
	</xsl:template>

	<xsl:template match="record">
		<mods:mods>
			<!--	<mods:titleInfo/>	-->
			<xsl:apply-templates select="Title"/>
			<xsl:apply-templates select="AlternativeTitle"/>
			<xsl:call-template name="generateAltTitles"/>
			
			<!--	<mods:name/>	-->
			<xsl:apply-templates select="People"/>
			<xsl:apply-templates select="Creator"/>
			<xsl:apply-templates select="Contributors"/>
			
			<!--	<mods:typeOfResource/>	-->
			<xsl:apply-templates select="DocType"/>
			
			<!--	<mods:genre/>	-->
			<xsl:call-template name="Genre"/>
			
			<!--	<mods:originInfo/>	-->
			<xsl:call-template name="CreationInfo"/>
			<xsl:call-template name="PublicationInfo"/>
			
			<!--	<mods:language/>	-->
			<xsl:call-template name="Language"/>
			
			<!--	<mods:physicalDescription/>	-->
			<xsl:apply-templates select="PhysicalDescription"/>
			
			<!--	<mods:abstract/>	-->
			<xsl:apply-templates select="Context"/>	
			
			<!--	<mods:tableOfContents/>	-->			
			<xsl:call-template  name="TableOfContents"/>
			
			<!--	<mods:note/>	-->
			<mods:note type="statement of responsibility"><xsl:value-of select="normalize-space(substring-after(Title,'/ '))"/></mods:note>
			<xsl:apply-templates select="Notes"/>
			<xsl:apply-templates select="Documentation"/>
			<xsl:apply-templates select="Illustrations"/>
			
			<xsl:call-template name="Price"/>
			
			<!--	<mods:subject/>	-->			
			<xsl:apply-templates select="Subjects"/>
			<xsl:apply-templates select="GeographicalLocation"/>
			
			<!--	<mods:relatedItem/>	-->			
			<xsl:call-template name="getRelatedItems"/>
			
			<!--	<mods:identifier/>	-->			
			<xsl:apply-templates select="ITMAReference"/>	
			<xsl:apply-templates select="CatalogueNumber"/>				
			<xsl:apply-templates select="InternalLink"/>
			<mods:identifier type="local">CID-<xsl:value-of select="@CID"/></mods:identifier>
			
			<!--	<mods:location/>	-->
			<xsl:apply-templates select="ArchiveLocation"/>	
			<xsl:apply-templates select="AlsoHeldAt"/>
			
			<!--	<mods:accessCondition/>	-->
			<xsl:call-template name="Copyright"/>
			
			<!--	<mods:recordInfo/>	-->
			<xsl:call-template name="recordInfo"/>
			
		</mods:mods>
	</xsl:template>

	<xsl:template match="Title">
		<xsl:variable name="titleProper" select="substring-before(substring-before(.,'/'),'[sound recording]')"/>
		<mods:titleInfo>
			<xsl:choose>
				<xsl:when test="$titleProper != ''">
					<mods:title><xsl:value-of select="normalize-space($titleProper)"/></mods:title>
				</xsl:when>
				<xsl:otherwise><mods:title><xsl:value-of select="."/></mods:title></xsl:otherwise>
			</xsl:choose>
		</mods:titleInfo>
	</xsl:template>
	
	<xsl:template match="AlternativeTitle">
		<xsl:variable name="titleProper" select="substring-before(substring-before(.,'/'),'[sound recording]')"/>
		<mods:titleInfo type="alternative">
			<xsl:choose>
				<xsl:when test="$titleProper != ''">
					<mods:title><xsl:value-of select="normalize-space($titleProper)"/></mods:title>
				</xsl:when>
				<xsl:otherwise><mods:title><xsl:value-of select="."/></mods:title></xsl:otherwise>
			</xsl:choose>
		</mods:titleInfo>
	</xsl:template>	
	
	<xsl:template name="generateAltTitles">
		<xsl:variable name="titleProper" select="substring-before(substring-before(Title,'/'),'[sound recording]')"/>
		<xsl:if test="substring-before($titleProper,'=')">
			<mods:titleInfo type="alternative">
				<mods:title><xsl:value-of select="normalize-space(substring-before($titleProper,'='))"/></mods:title>
			</mods:titleInfo>
			<mods:titleInfo type="alternative">
				<mods:title><xsl:value-of select="normalize-space(substring-after($titleProper,'='))"/></mods:title>
			</mods:titleInfo>			
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="People">
		<mods:name type="personal">
			<mods:namePart type="given"><xsl:value-of select="substring-before(.,' ')"/></mods:namePart>
			<mods:namePart type="family"><xsl:value-of select="substring-after(.,' ')"/></mods:namePart>
		</mods:name>
	</xsl:template>

	<xsl:template match="Creator">
		<mods:name>
			<mods:namePart><xsl:value-of select="."/></mods:namePart>
			<mods:role>
				<mods:roleTerm authority='marcrelator' authorityURI='http://id.loc.gov/vocabulary/relators' type='text' valueURI='http://id.loc.gov/vocabulary/relators/cre'>Creator</mods:roleTerm>
			</mods:role>
		</mods:name>
	</xsl:template>

	<xsl:template match="Contributors">
		<mods:name>
			<mods:namePart><xsl:value-of select="."/></mods:namePart>
			<mods:role>
				<mods:roleTerm authority='marcrelator' authorityURI='http://id.loc.gov/vocabulary/relators' type='text' valueURI='http://id.loc.gov/vocabulary/relators/ctb'>Contributor</mods:roleTerm>
			</mods:role>
		</mods:name>
	</xsl:template>

	<xsl:template name="Genre">
		<mods:genre authority="aat" type="Concept" displayLabel="Format" authorityURI="http://vocab.getty.edu/aat/" valueURI="http://vocab.getty.edu/aat/300374971">tape reels</mods:genre>
	</xsl:template>

	<xsl:template match="DocType">
		<xsl:if test=". = 'Image'">
			<mods:typeOfResource>still image</mods:typeOfResource>
		</xsl:if>
		<xsl:if test=". = 'Printed Material'">
			<mods:typeOfResource>text</mods:typeOfResource>
		</xsl:if>
		<xsl:if test=". = 'Sound Recording'">
			<mods:typeOfResource>sound recording</mods:typeOfResource>
		</xsl:if>	
		<xsl:if test=". = 'Video'">
			<mods:typeOfResource>moving image</mods:typeOfResource>
		</xsl:if>			
	</xsl:template>

	<xsl:template match="Context">
		<mods:abstract><xsl:value-of select="."/></mods:abstract>
	</xsl:template>

	<xsl:template match="GeographicalLocation">
		<mods:subject>
			<mods:geographic><xsl:value-of select="."></xsl:value-of></mods:geographic>
		</mods:subject>
	</xsl:template>
	
	<xsl:template match="InternalLink">
		<mods:location>
			<mods:url access="raw object"><xsl:value-of select="."/></mods:url>
		</mods:location>
	</xsl:template>

	<xsl:template match="ArchiveLocation">
			<mods:location>
				<mods:physicalLocation>Irish Traditional Music Archive</mods:physicalLocation>
				<mods:holdingSimple>
					<xsl:choose>
						<xsl:when test="substring-before(.,' -- ')">
							<mods:shelfLocator><xsl:value-of select="substring-before(.,' -- ')"/></mods:shelfLocator>
							<mods:shelfLocator><xsl:value-of select="substring-after(.,' -- ')"/></mods:shelfLocator>
						</xsl:when>
						<xsl:otherwise>
							<mods:shelfLocator><xsl:value-of select="."/></mods:shelfLocator>
						</xsl:otherwise>
					</xsl:choose>
				</mods:holdingSimple>
			</mods:location>
	</xsl:template>	
	
	<xsl:template match="PhysicalDescription">
		<mods:physicalDescription>
			<mods:extent><xsl:value-of select="."/></mods:extent>
			<xsl:if test="following-sibling::RunningTime">
				<mods:note type="running-time"><xsl:value-of select="following-sibling::RunningTime"/></mods:note>
			</xsl:if>
		</mods:physicalDescription>
	</xsl:template>

	<xsl:template match="Publisher">
		<xsl:if test="preceding-sibling::Publisher">
			<xsl:text> </xsl:text>
		</xsl:if>
		<xsl:value-of select="."/>
	</xsl:template>

	<xsl:template name="PublicationInfo">
		<xsl:variable name="publisher_info"><xsl:apply-templates select="Publisher"/></xsl:variable>
		
		<xsl:if test="PublisherLocation or Publisher or PublicationDate">
			<mods:originInfo eventType="publication">
				<xsl:if test="PublisherLocation">
					<mods:place>
						<mods:placeTerm type="text"><xsl:value-of select="PublisherLocation"/></mods:placeTerm>
					</mods:place>
				</xsl:if>
				<xsl:if test="Publisher">
					<mods:publisher><xsl:value-of select="$publisher_info"/></mods:publisher>
				</xsl:if>
				<xsl:if test="PublicationDate and PublicationDate[@nodate != '1']">
					<mods:dateIssued>
						<xsl:if test="PublicationDate/@qualifier">
							<xsl:attribute name="qualifier"><xsl:value-of select="PublicationDate/@qualifier"/></xsl:attribute>
						</xsl:if>
						<xsl:if test="PublicationDate/@encoding">
							<xsl:attribute name="encoding"><xsl:value-of select="PublicationDate/@encoding"/></xsl:attribute>
						</xsl:if>						
						<xsl:value-of select="PublicationDate/text()"/>
					</mods:dateIssued>
				</xsl:if>
			</mods:originInfo>
		</xsl:if>
	</xsl:template>

	<xsl:template name="CreationInfo">
		<xsl:if test="CreationLocation or CreationDate">
			<mods:originInfo eventType="creation">
				<xsl:if test="CreationLocation">
					<mods:place>
						<mods:placeTerm type="text"><xsl:value-of select="CreationLocation"/></mods:placeTerm>
					</mods:place>
				</xsl:if>
				<xsl:if test="CreationDate and CreationDate[@nodate != '1']">
					<mods:dateCreated>
						<xsl:if test="CreationDate/@qualifier">
							<xsl:attribute name="qualifier"><xsl:value-of select="CreationDate/@qualifier"/></xsl:attribute>
						</xsl:if>
						<xsl:if test="CreationDate/@encoding">
							<xsl:attribute name="encoding"><xsl:value-of select="CreationDate/@encoding"/></xsl:attribute>
						</xsl:if>	
						<xsl:value-of select="CreationDate"/>
					</mods:dateCreated>
				</xsl:if>
			</mods:originInfo>
		</xsl:if>
	</xsl:template>

	<xsl:template match="Notes">
		<mods:note><xsl:value-of select="."/></mods:note>
	</xsl:template>
	
	<xsl:template match="Documentation">
		<mods:note type="documentation"><xsl:value-of select="."/></mods:note>
	</xsl:template>

	<xsl:template match="Illustrations">
		<mods:note type="illustrations"><xsl:value-of select="."/></mods:note>
	</xsl:template>

	<xsl:template match="TypeOfSource">
		<mods:note type="accrual method"><xsl:value-of select="."/></mods:note>
	</xsl:template>

	<xsl:template name="Language">
		<xsl:if test="Language">
			<mods:language>
				<xsl:for-each select="Language">
					<mods:languageTerm	type="text"><xsl:value-of select="."/></mods:languageTerm>
				</xsl:for-each>
			</mods:language>
		</xsl:if>
	</xsl:template>

	<xsl:template name="Copyright">
		<mods:accessCondition type="use and reproduction">Copyright <xsl:value-of select="Copyright"/></mods:accessCondition>
		<mods:accessCondition type="use and reproduction" xlinkhref="http://rightsstatements.org/vocab/InC/1.0/">This item is protected by copyright and/or related rights. You are free to use this Item in any way that is permitted by the copyright and related rights legislation that applies to your use. For other uses you need to obtain permission from the rights-holder(s).</mods:accessCondition>
	</xsl:template>
	
	<xsl:template match="MatrixNumber">
		<mods:identifier type="matrix number">
			<xsl:value-of select="."></xsl:value-of>
		</mods:identifier>
	</xsl:template>
	
	<xsl:template name="TableOfContents">
		<xsl:variable name="contents_concat"><xsl:apply-templates select="Contents"/></xsl:variable>
		
		<xsl:if test="$contents_concat != ''">
			<mods:tableOfContents>
				<xsl:value-of select="$contents_concat"/>
			</mods:tableOfContents>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="Contents">
		<xsl:if test="preceding-sibling::Contents">
			<xsl:text> -- </xsl:text>
		</xsl:if>
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template name="getRelatedItems">			
		<xsl:for-each select="*[starts-with(name(),'Track')]">
			<mods:relatedItem type="constituent">
				<xsl:attribute name="ID">DMD_reel01_band00<xsl:value-of select="position()"/></xsl:attribute>
				<mods:tableOfContents><xsl:value-of select="."></xsl:value-of></mods:tableOfContents>
			</mods:relatedItem>
		</xsl:for-each>	

		<xsl:for-each select="Contents">
			<mods:relatedItem type="constituent">
				<mods:titleInfo>
					<mods:title><xsl:value-of select='.'/></mods:title>
				</mods:titleInfo>
			</mods:relatedItem>
		</xsl:for-each>
				
		<xsl:if test="ReIssue">
			<mods:relatedItem type="otherFormat">
				<mods:note type="reissue"><xsl:value-of select="ReIssue"/></mods:note>
			</mods:relatedItem>
		</xsl:if>

		<xsl:if test="PreIssue">
			<mods:relatedItem type="otherFormat">
				<mods:note type="preissue"><xsl:value-of select="PreIssue"/></mods:note>
			</mods:relatedItem>
		</xsl:if>

		<xsl:if test="CollectionTitle">
			<mods:relatedItem type="host" displayLabel="Collection">
				<mods:titleInfo>
					<mods:title><xsl:value-of select="CollectionTitle"/></mods:title>
				</mods:titleInfo>
			</mods:relatedItem>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="Subjects">
			<xsl:choose>
				<xsl:when test="substring-before(.,':')">
					<mods:subject>
						<mods:geographic><xsl:value-of select="substring-before(.,':')"/></mods:geographic>
						<mods:topic><xsl:value-of select="substring-after(.,': ')"/></mods:topic>
					</mods:subject>
				</xsl:when>	
				<xsl:otherwise>
					<xsl:if test=". != ../GeographicLocation">
						<mods:subject>
							<mods:topic><xsl:value-of select='.'/></mods:topic>
						</mods:subject>			
					</xsl:if>
				</xsl:otherwise>
			</xsl:choose>
	</xsl:template>
	
	<xsl:template match="ITMAReference">
		<mods:identifier type="local">
			<xsl:value-of select="."/>
		</mods:identifier>
	</xsl:template>

	<xsl:template match="CatalogueNumber">
		<mods:identifier type="music publisher">
			<xsl:value-of select="."/>
		</mods:identifier>
	</xsl:template>

	<xsl:template name="recordInfo">
		<mods:recordInfo>
			<xsl:choose>
				<xsl:when test="InformationSource">
					<mods:recordContentSource><xsl:value-of select="InformationSource"/></mods:recordContentSource>
				</xsl:when>
				<xsl:otherwise>
					<mods:recordContentSource>Irish Traditional Music Archive</mods:recordContentSource>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:if test="CataloguedBy">
				<mods:recordContentSource><xsl:value-of select="CataloguedBy"/></mods:recordContentSource>
			</xsl:if>
			<mods:recordOrigin>human prepared</mods:recordOrigin>
			<mods:descriptionStandard type="marcdescription">aacr</mods:descriptionStandard>		
		</mods:recordInfo>
	</xsl:template>

	<xsl:template name="Price">
		<xsl:if test="Price">
			<mods:note type="price"><xsl:value-of select="Price"/></mods:note>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="AlsoHeldAt">
		<mods:location>
			<mods:holdingSimple>
				<mods:copyInformation>
					<mods:note type="also held at"><xsl:value-of select="."/></mods:note>
				</mods:copyInformation>	
			</mods:holdingSimple>
		</mods:location>
	</xsl:template>
	
	
	<xsl:template name="tokenize">
		<xsl:param name="pText" select="."/>
		<xsl:variable name="delimiter" select="'&lt;br/&gt;'"/>		
		<xsl:if test="string-length($pText) >0">
			<mods:titleInfo>
				<mods:title>
					<xsl:value-of select="substring-before(concat($pText, $delimiter), $delimiter)"/>
				</mods:title>
			</mods:titleInfo>
			<xsl:call-template name="tokenize">
				<xsl:with-param name="pText" select=
					"substring-after($pText, $delimiter)"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>		
	
</xsl:stylesheet>
