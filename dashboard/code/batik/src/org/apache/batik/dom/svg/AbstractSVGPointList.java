/*

   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

 */
package org.apache.batik.dom.svg;

import org.apache.batik.parser.ParseException;
import org.apache.batik.parser.PointsHandler;
import org.apache.batik.parser.PointsParser;
import org.w3c.dom.DOMException;
import org.w3c.dom.svg.SVGException;
import org.w3c.dom.svg.SVGPoint;
import org.w3c.dom.svg.SVGPointList;

/**
 * Abstract implementation of {@link SVGPointList}.
 *
 * @author <a href="mailto:nicolas.socheleau@bitflash.com">Nicolas Socheleau</a>
 * @version $Id: AbstractSVGPointList.java 1831635 2018-05-15 13:33:47Z ssteiner $
 */
public abstract class AbstractSVGPointList
    extends AbstractSVGList
    implements SVGPointList {

    /**
     * Separator for a point list.
     */
    public static final String SVG_POINT_LIST_SEPARATOR
        = " ";

    /**
     * Return the separator between points in the list.
     */
    protected String getItemSeparator() {
        return SVG_POINT_LIST_SEPARATOR;
    }

    /**
     * Create an SVGException when the checkItemType fails.
     * @return SVGException
     */
    protected abstract SVGException createSVGException(short type,
                                                       String key,
                                                       Object[] args);

    /**
     * <b>DOM</b>: Implements {@link SVGPointList#initialize(SVGPoint)}.
     */
    public SVGPoint initialize(SVGPoint newItem)
            throws DOMException, SVGException {
        return (SVGPoint) initializeImpl(newItem);
    }

    /**
     * <b>DOM</b>: Implements {@link SVGPointList#getItem(int)}.
     */
    public SVGPoint getItem(int index) throws DOMException {
        return (SVGPoint) getItemImpl(index);
    }

    /**
     * <b>DOM</b>: Implements {@link
     * SVGPointList#insertItemBefore(SVGPoint,int)}.
     */
    public SVGPoint insertItemBefore(SVGPoint newItem, int index)
            throws DOMException, SVGException {
        return (SVGPoint) insertItemBeforeImpl(newItem,index);
    }

    /**
     * <b>DOM</b>: Implements {@link
     * SVGPointList#replaceItem(SVGPoint,int)}.
     */
    public SVGPoint replaceItem(SVGPoint newItem, int index)
            throws DOMException, SVGException {
        return (SVGPoint) replaceItemImpl(newItem,index);
    }

    /**
     * <b>DOM</b>: Implements {@link SVGPointList#removeItem(int)}.
     */
    public SVGPoint removeItem(int index) throws DOMException {
        return (SVGPoint) removeItemImpl(index);
    }

    /**
     * <b>DOM</b>: Implements {@link SVGPointList#appendItem(SVGPoint)}.
     */
    public SVGPoint appendItem(SVGPoint newItem)
            throws DOMException, SVGException {
        return (SVGPoint) appendItemImpl(newItem);
    }

    /**
     * Creates a new {@link SVGItem} object from the given {@link SVGPoint}.
     */
    protected SVGItem createSVGItem(Object newItem) {
        SVGPoint point = (SVGPoint) newItem;
        return new SVGPointItem(point.getX(), point.getY());
    }

    /**
     * Parses the 'points' attribute.
     *
     * @param value 'points' attribute value
     * @param handler point list handler
     */
    protected void doParse(String value, ListHandler handler)
            throws ParseException {
        PointsParser pointsParser = new PointsParser();
        PointsListBuilder builder = new PointsListBuilder(handler);
        pointsParser.setPointsHandler(builder);
        pointsParser.parse(value);
    }

    /**
     * Asserts that the given item is an {@link SVGPoint}.
     */
    protected void checkItemType(Object newItem) throws SVGException {
        if (!(newItem instanceof SVGPoint)) {
            createSVGException(SVGException.SVG_WRONG_TYPE_ERR,
                               "expected.point", null);
        }
    }

    /**
     * Helper class to interface the {@link PointsParser} and the
     * {@link PointsHandler}.
     */
    protected static class PointsListBuilder implements PointsHandler {

        /**
         * The {@link ListHandler} to pass newly created {@link SVGPointItem}
         * objects to.
         */
        protected ListHandler listHandler;

        /**
         * Creates a new PointsListBuilder.
         */
        public PointsListBuilder(ListHandler listHandler) {
            this.listHandler = listHandler;
        }

        /**
         * Implements {@link PointsHandler#startPoints()}.
         */
        public void startPoints() throws ParseException {
            listHandler.startList();
        }

        /**
         * Implements {@link PointsHandler#point(float,float)}.
         */
        public void point(float x, float y) throws ParseException {
            listHandler.item(new SVGPointItem(x, y));
        }

        /**
         * Implements {@link PointsHandler#endPoints()}.
         */
        public void endPoints() throws ParseException {
            listHandler.endList();
        }
    }
}
